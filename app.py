from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

parking_lot_status = {}
ticket_id_counter = 0


@app.route('/entry', methods=['POST'])
def entry():
    global ticket_id_counter
    licensePlate = request.args.get('plate')
    parkingLot = request.args.get('parkingLot')
    current_ticket_id = ticket_id_counter
    parking_lot_status[current_ticket_id] = {
        'license_plate': licensePlate,
        'parking_lot_name': parkingLot,
        'entry_time': datetime.datetime.now()
    }
    ticket_id_counter += 1
    return jsonify({'ticket_id': current_ticket_id})


@app.route('/exit', methods=['POST'])
def exit():
    ticketId = int(request.args.get('ticketId'))
    if ticketId not in parking_lot_status:
        return jsonify({'error': 'Ticket ID does not exists'})
    exit_time = datetime.datetime.now()
    parked_time_minutes = (exit_time - parking_lot_status[ticketId]['entry_time']).total_seconds() / 60.0
    charge = round((parked_time_minutes / 60.0) * 10, 2)
    result = jsonify({
        'license_plate': parking_lot_status[ticketId]['license_plate'],
        'parking_lot_name': parking_lot_status[ticketId]['parking_lot_name'],
        'parked_time_minutes': parked_time_minutes,
        'charge': charge
    })
    del parking_lot_status[ticketId]
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




