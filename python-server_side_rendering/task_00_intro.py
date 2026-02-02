def generate_invitations(template, attendees):
    """
    Generate personalized invitation files from a template and list of attendees.
    
    Args:
        template (str): Template string with placeholders
        attendees (list): List of dictionaries containing attendee information
    """
    # Check input types
    if not isinstance(template, str):
        print("Error: Template must be a string")
        return
    
    if not isinstance(attendees, list):
        print("Error: Attendees must be a list of dictionaries")
        return
    
    # Check if attendees is a list of dictionaries
    if attendees and not all(isinstance(attendee, dict) for attendee in attendees):
        print("Error: Attendees must be a list of dictionaries")
        return
    
    # Handle empty inputs
    if not template:
        print("Template is empty, no output files generated.")
        return
    
    if not attendees:
        print("No data provided, no output files generated.")
        return
    
    # Process each attendee
    for index, attendee in enumerate(attendees, start=1):
        # Create a copy of the template for this attendee
        output = template
        
        # Replace placeholders with actual values or "N/A" if missing
        output = output.replace("{name}", str(attendee.get("name") or "N/A"))
        output = output.replace("{event_title}", str(attendee.get("event_title") or "N/A"))
        output = output.replace("{event_date}", str(attendee.get("event_date") or "N/A"))
        output = output.replace("{event_location}", str(attendee.get("event_location") or "N/A"))
        
        # Generate output file
        filename = f"output_{index}.txt"
        try:
            with open(filename, 'w') as file:
                file.write(output)
            print(f"Generated: {filename}")
        except Exception as e:
            print(f"Error writing {filename}: {e}")
