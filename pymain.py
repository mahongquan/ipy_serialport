import sys
print(sys.path)
import getpath
sys.path.insert(0,getpath.getpath())
print(sys.path)
import main2
main2.main()