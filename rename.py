# -*- coding:UTF-8 -*-
# $$(CC_WRAPPER) $$(CC) $$(CFLAGS) $$(CFLAGS_LIB_$1) $$(CC_SDA_FLAGS) -C -E $$< > $$(<:.c=.e)
# python list.py D:\6947_cpc3815\vxworks-6.9\target\src\drv\sio .e
import sys
import os
import io

def lsdir(dstdir,fileext,newfileext):
	if(fileext=='.c'):
		mustexists='.raw'
		
	if(fileext=='.cc2'):
		mustexists='.c'
				
	if(fileext=='.raw'):
		mustexists='.c'

	if(fileext=='.cc'):
		mustexists='.c'

	curdir=dstdir;
	for ent in os.listdir(dstdir):
		curdir=os.path.join(dstdir,ent)
		if(os.path.isdir(curdir)):			
			lsdir(curdir,fileext,newfileext)
		
		
		if(curdir.find(fileext,(len(curdir)-len(fileext)),len(curdir)) != -1 ):
			pat1=(os.path.basename(curdir).replace('.e','.c'))
			allfiles_str=''.join(allfiles)
			
			
			if( os.path.exists(os.path.splitext(curdir)[0]+mustexists) and os.path.exists(os.path.splitext(curdir)[0]+newfileext)):				
				print('pass:'+curdir)
				os.remove(os.path.splitext(curdir)[0]+newfileext)
				os.rename(curdir,os.path.splitext(curdir)[0]+newfileext)
			else:	
				print(os.path.splitext(curdir)[0]+newfileext)							
				os.rename(curdir,os.path.splitext(curdir)[0]+newfileext)
			

# python3 clean.py . .raw .c	

if __name__ == "__main__":
	src_ext=sys.argv[2]
	dst_ext=sys.argv[3]
	with open('std.log.tmp','r') as frd:
		allfiles=frd.readlines()
		for file in allfiles:
			dir,ext=os.path.splitext(file)
			#print(dir+src_ext)
			if(os.path.exists(dir+src_ext)):
				if(os.path.exists(dir+dst_ext)):
					print(dir+dst_ext+' exists')
					os.remove(dir+dst_ext)
					os.rename(dir+src_ext,dir+dst_ext)
				else:
					print(dir+dst_ext+' not exists')
					os.rename(dir+src_ext,dir+dst_ext)
	#lsdir(sys.argv[1],sys.argv[2],sys.argv[3])		
