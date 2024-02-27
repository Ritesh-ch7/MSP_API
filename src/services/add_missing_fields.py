def add_missing_fields(reference_item):
        all_fields = ['ticket_type', 'service', 'priority', 'severity', 'requester_name', 'text', 'ticket_id']
        for key in all_fields:
                if key not in reference_item:
                        reference_item[key] = ''
        return reference_item 

