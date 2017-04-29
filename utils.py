import requests
import zipfile

def download_file(url, name):
    print("Downloading from: " + url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        print ("Saving to: " + name)
        with open(name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        print r


def unzip_file(file_name):
    fh = open(file_name, 'rb')
    z = zipfile.ZipFile(fh)
    names = []
    for name in z.namelist():
        outpath = file_name.replace(".zip", "") + "/"
        z.extract(name, outpath)
        names.append(outpath + name)
    fh.close()
    return names