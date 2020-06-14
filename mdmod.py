import os, sys, logging, re, shutil
from urllib.parse import unquote

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def parse_img(file):
    '''
    This function does two things:
    - Copy all images in the file and put in /mdpub-tmp folder
    - Edit all image references in the file to match Jekyll directory structure which is /static/img/{title name}/{img name}
    '''

    def read(file):
        '''
        This function reads and parse a Markdown file.
        It returns a string object.
        '''

        # Check if file exists and is a Markdown file
        if not (os.path.exists(file) and os.path.isfile(file) and file.lower().endswith('.md')):
            message = f"File check FAILED. Please check Filename argument: '{file}''"
            logger.critical(message)
            sys.exit("Exiting..")
        else:
            title = os.path.basename(file)[:-3]
            logger.info(f'Title = {title}')

        file = open(file, 'r')
        File = file.read()
        file.close()

        # Add Front Matters
        fmatter = f'---\nlayout: posts\ntitle: {title}\n---\n\n'
        File = fmatter + File

        return File

    file = os.path.abspath(file)
    Filestring = read(file)
    fileDir = os.path.dirname(file)
    title = os.path.basename(file)[:-3]
    os.chdir(fileDir)

    # Find Images
    matches = re.compile(r'!\[.*\]\(.*\)').findall(Filestring)

    # Handle possible URL encodings
    images = []
    for match in matches:
        image = unquote(match)
        images.append(image)
    imagesNo = str(len(images))


    logger.info(f'Found {imagesNo} images in Markdown files.')
    for image in images:
        logger.info(image)

    # Copy image files to /mdpub-tmp
    tmp = os.getcwd() + os.sep + 'mdpub-tmp/'
    logger.info(f'Staging images to {tmp}..')
    for image in images:
        img = image[4:-1]
        if img.startswith('.'):
            img = fileDir + img[1:]
        img_dest = tmp + os.path.basename(img)
        shutil.copy(img, img_dest)

    # Change Image references to Jekyll dir i.e static/img/{title}/
    jekyllDir = f'/static/img/{title}/'
    for match in matches:
        img = match[4:-1]
        image2 = unquote(jekyllDir + os.path.basename(img))
        logger.info(f'Replacing {img} with {image2}..')
        Filestring = Filestring.replace(img, image2)
    
    # Save as new MD file in tmp
    newfile = tmp + title + '.md'
    logger.info(f'Saving as {newfile}..')
    with open(newfile, 'w') as newfile:
        newfile.write(Filestring)
    
parse_img(sys.argv[1])


