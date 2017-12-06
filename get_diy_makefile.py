
# python3 py3.py dix/ .c > xmake.lua
import os
import os.path
import sys

logfile='ok.log'

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
	alllogcc=[]
	with open(logfile,'r') as logrd:
		loglns=logrd.readlines()
		get_dir='false'
		tmp_dir=''
		for logln in loglns:
			if(logln.find(': Entering directory') > 0):				
				get_dir='true'
				#print(logln)
				tmp_dir=logln

			if(logln.find(logpatern)==0):
				
				if(get_dir=='true'):
					curdir=(tmp_dir.split('\'')[1])
					get_dir='false'

				logln=logln.replace(logpatern,'')
				
				'''
				lns=logln.split(' ')
				lns_len=len(lns)
				srcname=lns[lns_len - 1]
				
				del lns[lns_len - 1]
				del lns[lns_len - 2]
				del lns[lns_len - 3]
				del lns[lns_len - 4]
				del lns[lns_len - 5]
				del lns[lns_len - 6]
				
				del lns[lns_len - 7]
				del lns[lns_len - 8]
				del lns[lns_len - 9]
				del lns[lns_len - 10]				
				'''			
				alllogcc.append(curdir+'::'+logln)

	return(alllogcc)

# deal all ents
def ccprehand(allccs):
	tmpccs=[]
	for ent in allccs:
		if(ent.find('test -f') > 0):

			pass
			s1=(ent.split('test -f'))[0].split('`')[0]
			s2=s1.split(' ')
			s2_len=len(s2)
			#print(s2)
			del s2[s2_len-1]
			del s2[s2_len-2]
			#del s2[s2_len-3]
			s3=' '.join(s2)

			t1=ent.split('test -f')[1]
			t2=t1.split('\'')[1]
			#print(t2)

			s4=s3+' '+t2.replace('.c','.o')+' '+t2
			#print(s4)

			'''
			old='-g -O2'
			new='-D_VSB_CONFIG_FILE=\"D:/wr/20170315/workbench-4/workspace/vsb_generic/h/config/vsbConfig.h\" '
			new=new+'-isystemD:/wr/20170315/workbench-4/workspace/vsb_generic/krnl/h/public '
			new=new+'-isystemD:/wr/20170315/workbench-4/workspace/vsb_generic/krnl/h/system '
			new=new+'-ID:/wr/20170315/workbench-4/workspace/vsb_generic/share/h '
			new=new+old
		
			s4.replace('-g -O2',new)		
			'''
			tmpccs.append(s4)

		else:
			pass
			
			s2=ent.split(' ')
			s2_len=len(s2)
			t2=s2[s2_len-1].split('\n')[0]
			
			del s2[s2_len-1]
			del s2[s2_len-2]
			#del s2[s2_len-3]
			s3=' '.join(s2)
			
			s4=s3+' '+t2.replace('.c','.o')+' '+t2
		
				
			tmpccs.append(s4)			
			
	return (tmpccs)

# python3 get_diy_makefile.py std.log diy_makefile
# make -f diy_makefile
if (__name__=='__main__'):

	if(len(sys.argv) < 2):
		print('sys argv < 2')
		sys.exit(0)	
	
	logfile=sys.argv[1]
	print('in  file is:'+logfile)
	print('out file is:'+sys.argv[2])

	outent=[]

	with open(logfile,'r') as frd:

		alllog1 = frd.readlines()
		frd.close()
	
	
	out=[]
	out.append('all:	')
	for log in alllog1:
		
		if(len(log.split('::')) == 2):
			dir  = log.split('::')[0]
			str= log.split('::')[1]
			strs=(str.split(' '))
			strs_len=len(strs)

			ccfilename=strs[strs_len-1].split('\n')[0]

			if(ccfilename.find('./') > 0):
				ccfilename=(ccfilename.split('`')[1])

			del strs[strs_len-1]
			del strs[strs_len-2]
			del strs[strs_len-3]
			del strs[strs_len-4]

			out_str1='	cd '+dir+' && gcc'
			out_str2=(' '.join(strs))+' -E -C -dD '
			out_str2=out_str2+ccfilename+' > '+ccfilename.replace('.c','.e')

			#print(out_str1+out_str2)
			out.append(out_str1+out_str2)
		else:
			pass


	
	out.append('e-clean:	')
	for log in alllog1:
		if(len(log.split('::')) == 2):
			dir  = log.split('::')[0]
			str= log.split('::')[1]
			strs=(str.split(' '))
			strs_len=len(strs)
			
			ccfilename=strs[strs_len-1].split('\n')[0]
			if(ccfilename.find('./') > 0):
				ccfilename=(ccfilename.split('`')[1])

			del strs[strs_len-1]
			del strs[strs_len-2]
			del strs[strs_len-3]
			del strs[strs_len-4]


			out_str1='	rm -rf '+os.path.join(dir,ccfilename.replace('.c','.e'))			

			out.append(out_str1)	

	out.append('cc-clean:	')
	for log in alllog1:
		if(len(log.split('::')) == 2):
			dir  = log.split('::')[0]
			str= log.split('::')[1]
			strs=(str.split(' '))
			strs_len=len(strs)
			
			ccfilename=strs[strs_len-1].split('\n')[0]
			if(ccfilename.find('./') > 0):
				ccfilename=(ccfilename.split('`')[1])

			del strs[strs_len-1]
			del strs[strs_len-2]
			del strs[strs_len-3]
			del strs[strs_len-4]

			out_str1='	rm -rf '+os.path.join(dir,ccfilename.replace('.c','.cc'))			
			out.append(out_str1)	

	out.append('cc2-clean:	')
	for log in alllog1:
		if(len(log.split('::')) == 2):
			dir  = log.split('::')[0]
			str= log.split('::')[1]
			strs=(str.split(' '))
			strs_len=len(strs)
			
			ccfilename=strs[strs_len-1].split('\n')[0]
			if(ccfilename.find('./') > 0):
				ccfilename=(ccfilename.split('`')[1])

			del strs[strs_len-1]
			del strs[strs_len-2]
			del strs[strs_len-3]
			del strs[strs_len-4]

			out_str1='	rm -rf '+os.path.join(dir,ccfilename.replace('.c','.cc2'))			
			out.append(out_str1)			
	with open(sys.argv[2],'w') as wrfp:
		wrfp.writelines('\n'.join(out))
		wrfp.close()

	
		
			
