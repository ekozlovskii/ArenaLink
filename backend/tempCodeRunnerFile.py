@app.route('/send_report_by_login/<string:login>', methods=['POST'])
def send_report_by_login(login):
    user = User.query.filter_by(login=login).first()
    if not user or user.role != 'organizer':
        return jsonify({'error': 'Organizer not found'}), 404
    if not user.email:
        return jsonify({'error': 'Email is not specified for the organizer'}), 400

    matches = Match.query.filter_by(created_by=user.id).all()
    if not matches:
        return jsonify({'error': 'No matches found for this organizer'}), 404

    data = [{
        'Match Name': m.match_name,
        'Date & Time': m.date_time.strftime('%Y-%m-%d %H:%M'),
        'Stadium': m.stadium_name,
        'Match Type': (m.match_type or '').capitalize(),
        'Tickets Left': m.ticket_quantity,
        'Ticket Price (₽)': float(m.ticket_price)
    } for m in matches]

    df = pd.DataFrame(data)

    subject = "📊 Match Report"
    body = (
        f"Hello {user.name},\n\n"
        f"Attached is your match report in Excel format.\n\n"
        f"Best regards,\nArenaLink Team"
    )

    send_email_with_excel(user.email, subject, body, df)
    return jsonify({'message': 'The match report was successfully sent to the organizer\'s email'}), 200


@app.route('/api/sectors/<int:stadium_id>', methods=['GET'])
def get_sectors_by_stadium(stadium_id):
    sectors = Sector.query.filter_by(stadium_id=stadium_id).all()
    return jsonify({
        "sectors": [s.name for s in sectors]
    })

