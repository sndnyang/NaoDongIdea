import mindmap as application

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    application.app.run(host="0.0.0.0", port=5002, debug=True)

