from flask import Flask, render_template, request, jsonify
from eth_account import Account
import os
import multiprocessing as mp

# Enable unaudited HD wallet features for eth-account
Account.enable_unaudited_hdwallet_features()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    prefix = (data.get('prefix') or '').lower().strip()
    suffix = (data.get('suffix') or '').lower().strip()
    # Remove optional 0x
    if prefix.startswith('0x'):
        prefix = prefix[2:]
    if suffix.startswith('0x'):
        suffix = suffix[2:]
    # Require at least one
    if not prefix and not suffix:
        return jsonify({'error': 'Please provide a prefix and/or suffix'}), 400
    # Validate hex
    for name, part in [('prefix', prefix), ('suffix', suffix)]:
        if part and not all(c in '0123456789abcdef' for c in part):
            return jsonify({'error': f"{name.capitalize()} must be hex characters"}), 400
    # Multi-process brute-force
    manager = mp.Manager()
    result_queue = manager.Queue()
    stop_event = manager.Event()
    def worker(prefix, suffix, result_queue, stop_event):
        while not stop_event.is_set():
            acct = Account.create(os.urandom(32))
            hexaddr = acct.address.lower()[2:]
            if prefix and not hexaddr.startswith(prefix):
                continue
            if suffix and not hexaddr.endswith(suffix):
                continue
            result_queue.put((acct.address, acct.key.hex()))
            stop_event.set()
            break

    num_workers = os.cpu_count() or 4
    processes = []
    for _ in range(num_workers):
        p = mp.Process(target=worker, args=(prefix, suffix, result_queue, stop_event))
        p.daemon = True
        p.start()
        processes.append(p)

    address, private_key = result_queue.get()
    # Terminate other workers
    for p in processes:
        if p.is_alive():
            p.terminate()
    return jsonify({
        'address': address,
        'private_key': private_key
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
