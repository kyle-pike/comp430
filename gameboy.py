# from pyboy import PyBoy

# Create an instance of PyBoy with the path to the Game Boy ROM
# rom_path = "pokemon.gbc"
# pyboy = PyBoy(rom_path)

# Run the emulation loop
# try:
# 	while not pyboy.tick():
# 		pass
# except KeyboardInterrupt:
	# Exit gracefully if the user interrupts the emulation
	# pyboy.stop()
import wget
url = 'https://vimm.net/vault/GBC'
wget.download(url)

rom_id = input('Enter ROM ID: ')
download_url = f'https://vimm.net/vault/{rom_id}'
wget.download(download_url)