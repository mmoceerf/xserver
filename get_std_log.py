
# python3 py3.py dix/ .c > xmake.lua
import os
import os.path
import sys

logfile='V1.make'

# str + full dir
def str2lua (ent,filedir):
	retlist=[]
	defines=[]
	includedirs=[]
	cxflags=[]
	filedir=(filedir.split('\n')[0])
	filedir=filedir.replace('\\','/')

	curoutfile2=os.path.dirname(filedir) # file dir
	#curoutfile2.replace('\\','/')

	fulldir=filedir # file full dir

	cuts=(ent.split(' '))
	cuts_len=len(cuts)
		
	for cut in cuts:

		#0 filter cxflags
		if(cut.find('ccpentium') == 0 or \
		   cut.find('-c') == 0 or \
		   cut.find('-o') == 0):
			continue

		#1 for include dir
		if(cut.find('-I') == 0):

			if(cut.find(':') != 3):
				
				#notice here wind path 2 linux path \ to /
				absdir=(os.path.join(curoutfile2,cut[2:]))
				absdir = os.path.abspath(absdir)
				acuts=absdir.split('\\')
				absdir='/'.join(acuts) 
				#print(includedirs)
				#print(absdir+'----------'+curoutfile2+'-------'+cut[2:])
				if(cut.find('-I..') == 0):
					
					inc2=((absdir))
					
					includedirs.append('"'+inc2+'"')

					#print(('"'+inc2+'",'))
					continue					
				if(cut.find('-I.') == 0):
					#print('i.f:'+absdir)
					inc1=((absdir)[:-1])
					includedirs.append('"'+inc1+'"')
					#print(('"'+inc1+'",'))
					continue
				
				if(ent.find('-I/usr/include/') > 0):
					#print(('"D:/wr/xmake/x"'+cut[2:]))
					includedirs.append('"D:/wr/xmake/x'+cut[2:]+'"')
					continue
				

				includedirs.append('"'+absdir+'"')
				continue
			else:
				pass
				#print('"else:'+curoutfile2+'",')		

			continue
		
		#2 for define 
		if(cut.find('-D') == 0):

			if(cut.find('-D_VSB_CONFIG_FILE=') == 0):
				re1= (cut.replace('\\','\\\\'))
				re2= (re1.replace('\"','\\\"'))			
	
			defines.append('"'+cut.replace('-D','')+'",')
			continue
		
		#3 for cxflags
		if(cut != ''):
			cxflags.append(' "'+cut+'",')

	includedirs.append('"D:/wr/xmake/x/usr/include"')
	str_includedirs='includedirs={'+(', '.join(includedirs))  +'}'
	#print(str_includedirs)
	#str_includedirs = (str_includedirs[0:len(str_includedirs)-1]) + '} '

	str_start='    add_files("'+fulldir+'",{'
	str_end='})'

	str_cxflags='cxflags={'+(''.join(cxflags)) # +'}, '
	str_cxflags = (str_cxflags[0:len(str_cxflags)-1]) + '}, '

	
	str_defines='defines={'+(''.join(defines)) #+'}, '
	str_defines = (str_defines[0:len(str_defines)-1]) + '}, '	
	
	

	
	#print((str_start+str_cxflags+str_defines+str_includedirs+str_end))
	return(str_start+str_cxflags+str_defines+str_includedirs+str_end)

def lsdir(dstdir,fileext):
	curdir=dstdir;
	fileDirs=[]
	for ent in os.listdir(dstdir):
		curdir=os.path.join(dstdir,ent)
		#print(curdir)
		if(os.path.isdir(curdir)):			
			lsdir(curdir,fileext)
		
		if(curdir.find(fileext,(len(curdir)-len(fileext)),len(curdir)) != -1 ):
			#print(curdir)
			fileDirs.append(curdir)
	return (fileDirs)

# curdir+'::'+logln
def getallcc(logfile):
	logpatern='/bin/bash ../libtool  --tag=CC   --mode=compile gcc'
	logpatern2='/bin/bash ../../../libtool  --tag=CC   --mode=compile gcc'
	alllogcc=[]
	allfiles=[]
	with open(logfile,'r') as logrd:
		loglns=logrd.readlines()
		get_dir='false'
		tmp_dir=''
		for logln in loglns:
			if(logln.find(': Entering directory') > 0):				
				get_dir='true'
				#print(logln)
				tmp_dir=logln

			if((logln.find(logpatern) == 0 or \
				logln.find(logpatern2) == 0 ) and \
			 	logln.find('test -f') > 0 ):

				cnts=(logln.split('`'))
				cnts_len=len(cnts)
				logln=(cnts[1]+' '+cnts[2])
				#print(logln)
				#alllogcc.append(curdir+'::'+tmp)
				#continue

			if(logln.find(logpatern) == 0 ):
				
				if(get_dir=='true'):
					curdir=(tmp_dir.split('\'')[1])
					get_dir='false'

				logln=logln.replace(logpatern,'')
				alllogcc.append(curdir+'::'+logln)

			if(logln.find(logpatern2) == 0):
				
				if(get_dir=='true'):
					curdir=(tmp_dir.split('\'')[1])
					get_dir='false'

				logln=logln.replace(logpatern2,'')

				filename=logln.split(' ')
				name=filename[len(filename)-1]
				logln=logln.split('-c -o')[0]

				tmp2=os.path.join(curdir,name)
				#print(os.path.exists(tmp2))
				#if(os.path.exists(tmp2)):
				allfiles.append(tmp2)
				alllogcc.append(curdir+'::'+logln+'-o '+name.replace('.c\n','.o')+' -c '+name.replace('.c\n','.c'))				

	with open(outfile+'.tmp','w') as fp:
		fp.writelines(allfiles)
		fp.close()
	return(alllogcc)

# python3 get_std_log.py raw.log std.log
if (__name__=='__main__'):

	if(len(sys.argv) < 2):
		print('sys argv < 2')
		sys.exit(0)	

	logfile=sys.argv[1]
	outfile=sys.argv[2]
	print('logfile is:'+logfile)
	print('outfile is:'+outfile)
	
	outent=[]
	alllog1 = getallcc(logfile)

	for ent in alllog1:
		outent.append(ent+'\n')

	with open(outfile,'w') as fwr:
		fwr.writelines(outent)
		fwr.close()


		
			
