import urllib2
import os
import sys
import shutil


def EnsureFileCanBeWritten(filename):
  directory = os.path.dirname(filename)
  if directory != '' and not os.path.exists(directory):
    os.makedirs(directory)
    
def WriteDataFromStream(filename, stream, chunk_size):
  EnsureFileCanBeWritten(filename)
  f = open(filename, 'wb')
  file_size_dl = 0
  content_len = int(stream.headers.get('Content-Length'))
  sys.stdout.write("Downloading: %s Bytes: %s\n" % (filename, content_len))
  try:
    while True:
      # Indicate that we're still writing.
      status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / content_len)
      status = status + chr(8)*(len(status)+1)
      sys.stdout.write(status)
      sys.stdout.flush()
      
      data = stream.read(chunk_size)
      data_len = len(data)
      if data_len == 0:
        break
      f.write(data)
      file_size_dl += data_len     
  finally:
    sys.stdout.write('\n')
    f.close()

def HttpDownload(url, target):
  """Download a file from a remote server.

  Args:
    url: A URL to download from.
    path: Filename to write download to.
  """
  logger = sys.stdout.write
  headers = [('Accept', '*/*')]
  if os.environ.get('http_proxy'):
    proxy = os.environ.get('http_proxy')
    proxy_handler = urllib2.ProxyHandler({
        'http': proxy,
        'https': proxy})
    opener = urllib2.build_opener(proxy_handler)
  else:
    opener = urllib2.build_opener()
  opener.addheaders = headers
  urllib2.install_opener(opener)
  # Retry up to 10 times (appengine logger is flaky).
  for i in xrange(10):
    if i:
      logger('Download failed on %s, retrying... (%d)\n' % (url, i))
    try:
      # 30 second timeout to ensure we fail and retry on stalled connections.
      src = urllib2.urlopen(url, timeout=30)
      content_len = src.headers.get('Content-Length')
      content_len = int(content_len)
      if os.path.isfile(target):
        if content_len == os.path.getsize(target):
          return
    
      try:
        targrt_tmp = target + '.tmp'
        WriteDataFromStream(targrt_tmp, src, chunk_size=2**20)        
        if content_len:         
          file_size = os.path.getsize(targrt_tmp)
          if content_len != file_size:
            logger('Filesize:%d does not match Content-Length:%d' % (
                file_size, content_len))
            continue
      finally:
        src.close()
        
      break
    except urllib2.HTTPError, e:
      if e.code == 404:
        logger('Resource does not exist.\n')
        raise
      logger('Failed to open.\n')
    except urllib2.URLError:
      logger('Failed mid stream.\n')
  else:
    logger('Download failed on %s, giving up.\n' % url)
    raise
  shutil.move(targrt_tmp, target)
  
def DownloadFile(url, path):
  try:
    HttpDownload(url, path)
  except Exception, e:
    return False
  return True