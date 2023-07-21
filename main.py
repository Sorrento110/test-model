import click
import random
import json
import time
import pandas as pd
from faker import Faker
from collections import OrderedDict
import urllib.request
import os
import requests
import xarray as xr
if not os.path.exists('output'):
    os.mkdir('output')

if not os.path.exists('media'):
    os.mkdir('media')    

@click.command()
@click.option('--temp', type=float, required=True, help='Percentage perturbation to temperature.')
def main(temp):
    params = open('configFiles/parameters.json').read()
    params = json.loads(params)

    configFileData = open('configFiles/fakeDataType.json').read()
    configFileData = json.loads(configFileData)


    print('Beginning to download file from S3...')

    url = 'https://jataware-world-modelers.s3.amazonaws.com/dummy-model/input.csv'
    urllib.request.urlretrieve(url, 'input.csv')


    locales = OrderedDict([
        ('en-US', 1)
    ])
    fake = Faker(locales)
    f = fake['en_US']    
    data = []

    perturbation = 1 + (params['rainfall']*temp)
    getColorHue = configFileData['color_hue']
    for i in range(100):
        obj = dict(latitude=f.latitude(),
                   longitude=f.longitude(),
                   date=f.date(),
                   value=random.random()*perturbation,
                   color_hue=f.color(hue=getColorHue))
        data.append(obj)

    df = pd.DataFrame(data)
    print(df.head())
    fname = f"output_{params['rainfall']}_{temp}"
    df.to_csv(f'output/{fname}.csv', index=False)
    print(f"Saved output as /model/output/{fname}.csv")

    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')

    # Step 1: Convert the pandas DataFrame to an xarray Dataset
    xr_dataset = xr.Dataset.from_dataframe(df.set_index('date'))

    # Step 2: Save the xarray Dataset to a NetCDF file
    xr_dataset.to_netcdf('output/output_file.nc')



def get_media():
    image_urls = ['https://i.kym-cdn.com/entries/icons/facebook/000/000/774/lime-cat.jpg',
                  'https://pbs.twimg.com/profile_images/1356088845821857795/1WWMDwIQ_400x400.jpg']
    for url in image_urls:
        filename = url.split('/')[-1]
        img_data = requests.get(url).content
        with open(f'media/{filename}', 'wb') as handler:
            handler.write(img_data)
        print(f"Wrote media: {filename}")
    return


if __name__ == "__main__":
    get_media()
    main()
    print("SUCCESS")
