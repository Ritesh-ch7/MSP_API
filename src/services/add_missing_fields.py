def add_missing_fields(reference_item):

        """
        Adds missing fields with empty values to the given reference item dictionary.
        
        Args:
        - reference_item: The dictionary representing a reference item.
        
        Returns:
        The updated dictionary with missing fields added and set to empty values.
        """
        
        all_fields = ['ticket_type', 'service', 'priority', 'severity', 'requester_name', 'text', 'ticket_id']
        for key in all_fields:
                if key not in reference_item:
                        reference_item[key] = ''
        return reference_item 

