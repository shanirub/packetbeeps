import time
from scapy.all import sniff

# flag for breaking event loop
stop_sniffing = False

# set to True only on raspi
play_buzzer = False

# Buzzer object only on raspi
buzzer = None

def is_raspberry_pi():
    """

    :return: True if running on raspi, False otherwise
    """
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            return 'Raspberry Pi' in model
    except FileNotFoundError:
        return False

def stop_filter(packet):
    global stop_sniffing
    return stop_sniffing

def calculate_tone(protocol, sport, dport, packet_size, ttl):
    """
    decide which tone to play, based on various packet's attributes
    :param protocol:
    :param sport: source port
    :param dport: dest port
    :param packet_size:
    :param ttl:
    :return: int 0-7 for a note
    """
    # Map protocol to a base note
    protocol_map = {
        "TCP": 0,  # C4
        "UDP": 1,  # D4
        "ICMP": 2  # E4
    }
    base_note = protocol_map.get(protocol, 0)  # Default to C4

    # Map source port and destination port to variations
    tone_offset = (sport + dport) % 8  # Map to one of 8 tones

    # Scale tone by packet size
    size_offset = (packet_size // 100) % 8  # Larger packets shift notes

    # Adjust for TTL
    ttl_shift = (ttl // 32) % 8  # Normalize TTL to a range

    # Calculate final tone index
    tone_index = (base_note + tone_offset + size_offset + ttl_shift) % 8

    return tone_index


def process_packets(packet_batch):
    """
    process all packets in batch, and calculate tone for each one
    on raspi a Buzzer() is created to allow actual beeps
    on pc only prints are shown
    """
    global buzzer
    print(f"Processing {len(packet_batch)} packets...")
    for packet in packet_batch:
        # get used values
        protocol = packet.sprintf("%IP.proto%") if packet.haslayer('IP') else "Unknown"
        sport = getattr(packet, 'sport', 0)
        dport = getattr(packet, 'dport', 0)
        size = len(packet)
        ttl = getattr(packet, 'ttl', 64)

        # find tone for values
        tone_index = calculate_tone(protocol, sport, dport, size, ttl)
        print(f"Playing tone index: {tone_index}")

        if play_buzzer and buzzer:
            # only on raspi
            buzzer.play_note(tone_index)


def main():
    global stop_sniffing
    global buzzer
    global play_buzzer
    play_buzzer= is_raspberry_pi()

    if play_buzzer:
        # only on raspi
        from buzzer import Buzzer
        buzzer = Buzzer()

    print(f"Running on raspi: {play_buzzer}. buzzer: {buzzer}")
    print("Starting packet sniffing... Ctrl+C to stop")
    try:
        while not stop_sniffing:
            print(f"stop sniffing is {stop_sniffing}")
            packets = sniff(count=10, timeout=5, stop_filter=stop_filter)  # Timeout ensures it doesn't hang if no packets are captured
            if packets:
                process_packets(packets)
            else:
                print("No packets captured in this cycle.")

            time.sleep(2) # taking a break from sniffing and allowing interruption
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected, stopping...")
        stop_sniffing = True

    print("Exiting gracefully.")

if __name__ == "__main__":
    main()

