import os
from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table

def Solve(catfn):
    catfnwcs=f'{os.path.splitext(catfn)[0]}_wcs.fits'
    os.system(f'python3 client.py -k bgqyiflmwpyxfscc -u {catfn} --newfits={catfnwcs}')

    rawtable=Table.read(catfn)
    hdr=fits.getheader(catfnwcs)

    w=WCS(hdr)

    x=rawtable['x']
    y=rawtable['y']
    sky=w.pixel_to_world(x,y)

    ra=sky.ra.deg
    dec=sky.dec.deg

    rawtable['ra']=ra
    rawtable['dec']=dec

    cat_hl=fits.HDUList([
        fits.PrimaryHDU(header=hdr),
        fits.BinTableHDU(data=rawtable)
    ])

    cat_hl.writeto(catfnwcs,overwrite=True)
