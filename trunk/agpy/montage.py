#!/usr/bin/env python
import optparse
import os,shutil
import glob
import tempfile
tempfile.tempdir = '/Volumes/disk4/var/tmp'
import sys
#print sys.path
#sys.path.remove('')
sys.path.remove(os.path.split(__file__)[0])
import montage


if __name__ == "__main__":

    parser=optparse.OptionParser()

    parser.add_option("--header",default='mosaic.hdr',help="Name of the .hdr file or a fits file from which to extract a header.  Defaults to mosaic.hdr")
    parser.add_option("--get-header","-g",default=False,action='store_true',help="Get the header of the first input file?  Overrides --header.  Default False")
    parser.add_option("--combine",default='median',help="How to combine the images.  Options are mean, median, count.  Default median")
    parser.add_option("--exact","--exact_size","--exact-size","-X",default=True,action='store_true',help="Use exact_size=True?  Default True")
    parser.add_option("--outfile","--out","-o",default=None,help="Output file name")
    parser.add_option("--copy",default=False,action='store_true',help="Copy files instead of linking")

    parser.set_usage("%prog outfile=filename.fits *.fits combine=median")
    parser.set_description(
    """
    Wrapper to mosaic a *subset* of images in the current directory
                                                                                           
    Usage:
    mGetHdr template_fitsfile.fit mosaic.hdr
    montage outfile=l089_reference_montage.fits 0*_indiv13pca*_map01.fits combine=median &
                                                                                           
    Keyword parameters:
      combine - 'median', 'average', or 'sum'
      header  - Filename of fits file from which to create mosaic.hdr
      outfile - Output fits filename
    """)

    options,args = parser.parse_args()

    if options.outfile is None:
        raise ValueError("Must specify outfile name")

    filelist = []
    for a in args:
        filelist += glob.glob(a)
        
    print filelist

    print "Creating temporary directory and hard-linking (not sym-linking) all files into it"
    #echo "Creating temporary directory and sym-linking all files into it"
    os.mkdir('tmp/')
    if options.copy:
        for fn in filelist:
            shutil.copy(fn,'tmp/%s' % fn)
        shutil.copy(options.header,'tmp/%s' % options.header)
    else:
        for fn in filelist:
            os.link(fn,'tmp/%s' % fn)
        os.link(options.header,'tmp/%s' % options.header)

    olddir = os.getcwd()
    os.chdir('tmp/')
    dir = os.getcwd()
    montage.wrappers.mosaic(dir,'%s/mosaic' % dir,header='%s/%s' % (dir,options.header), exact_size=options.exact, combine=options.combine)

    if os.path.exists('tmp/mosaic/mosaic.fits'):
        shutil.move('tmp/mosaic/mosaic.fits',options.outfile)
