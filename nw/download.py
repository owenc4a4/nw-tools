import urllib2
import os


def do_download(url, path):
  file_name = url.split('/')[-1]
  u = urllib2.urlopen(url)
  meta = u.info()
  file_size = int(meta.getheaders("Content-Length")[0])
  if os.path.isfile(path):
    if file_size == os.path.getsize(path):
      return
    
  print "Downloading: %s Bytes: %s" % (file_name, file_size)
  file_temp = path + '.tmp'
  f = open(file_temp, 'wb')
  file_size_dl = 0
  block_sz = 8192
  #download file
  while True:
      buffer = u.read(block_sz)
      if not buffer:
          break
  
      file_size_dl += len(buffer)
      f.write(buffer)
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
      status = status + chr(8)*(len(status)+1)
      print status,
  
  f.close()
  shutil.move(file_temp, path)

def DownloadFile(url, path): 
  do_download(url, path)