def add_missing_fields(reference_item):
        """
    Adds missing fields with empty values to a reference item.

    Args:
    - reference_item (dict): The reference item to be checked and updated.

    Returns:
    dict: The reference item with missing fields added and set to empty strings.
    """
        all_fields = ['ticket_type', 'service', 'priority', 'severity', 'requester_name', 'text', 'ticket_id']
        for key in all_fields:
                if key not in reference_item:
                        reference_item[key] = ''
        return reference_item 

