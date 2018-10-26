#!/usr/bin/python

import sys
import os
import random
import requests

from StringIO import StringIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from fpdf import FPDF

IMAGE_URL = 'http://loremflickr.com/1280/768/{0}'
IMAGE_CAT = ['business', 'fun', 'meme', 'enterprise', 'data', 'nature', 'money', 'team', 'diagram', 'industry']

# source: http://www.atrixnet.com/bs-generator.html
BS_ADVERBS = ['appropriately', 'assertively', 'authoritatively', 'collaboratively', 'compellingly', 'competently', 'completely', 'continually', 'conveniently', 'credibly', 'distinctively', 'dramatically', 'dynamically', 'efficiently', 'energistically', 'enthusiastically', 'fungibly', 'globally', 'holisticly', 'interactively', 'intrinsically', 'monotonectally', 'objectively', 'phosfluorescently', 'proactively', 'professionally', 'progressively', 'quickly', 'rapidiously', 'seamlessly', 'synergistically', 'uniquely']
BS_VERBS = ['actualize', 'administrate', 'aggregate', 'architect', 'benchmark', 'brand', 'build', 'cloudify', 'communicate', 'conceptualize', 'coordinate', 'create', 'cultivate', 'customize', 'deliver', 'deploy', 'develop', 'dinintermediate disseminate', 'drive', 'embrace', 'e-enable', 'empower', 'enable', 'engage', 'engineer', 'enhance', 'envisioneer', 'evisculate', 'evolve', 'expedite', 'exploit', 'extend', 'fabricate', 'facilitate', 'fashion', 'formulate', 'foster', 'generate', 'grow', 'harness', 'impact', 'implement', 'incentivize', 'incubate', 'initiate', 'innovate', 'integrate', 'iterate', 'leverage existing', 'leverage other\'s', 'maintain', 'matrix', 'maximize', 'mesh', 'monetize', 'morph', 'myocardinate', 'negotiate', 'network', 'optimize', 'orchestrate', 'parallel task', 'plagiarize', 'pontificate', 'predominate', 'procrastinate', 'productivate', 'productize', 'promote', 'provide access to', 'pursue', 'recaptiualize', 'reconceptualize', 'redefine', 're-engineer', 'reintermediate', 'reinvent', 'repurpose', 'restore', 'revolutionize', 'right-shore', 'scale', 'seize', 'simplify', 'strategize', 'streamline', 'supply', 'syndicate', 'synergize', 'synthesize', 'target', 'transform', 'transition', 'underwhelm', 'unleash', 'utilize', 'visualize', 'whiteboard']
BS_ADJECTIVES = ['24/7', '24/365', 'accurate', 'adaptive', 'alternative', 'an expanded array of', 'B2B', 'B2C', 'backend', 'backward-compatible', 'best-of-breed', 'bleeding-edge', 'bricks-and-clicks', 'business', 'clicks-and-mortar', 'client-based', 'client-centered', 'client-centric', 'client-focused', 'cloud-based', 'cloud-centric', 'cloudified', 'collaborative', 'compelling', 'competitive', 'cooperative', 'corporate', 'cost effective', 'covalent', 'cross functional', 'cross-media', 'cross-platform', 'cross-unit', 'customer directed', 'customized', 'cutting-edge', 'distinctive', 'distributed', 'diverse', 'dynamic', 'e-business', 'economically sound', 'effective', 'efficient', 'elastic', 'emerging', 'empowered', 'enabled', 'end-to-end', 'enterprise', 'enterprise-wide', 'equity invested', 'error-free', 'ethical', 'excellent', 'exceptional', 'extensible', 'extensive', 'flexible', 'focused', 'frictionless', 'front-end', 'fully researched', 'fully tested', 'functional', 'functionalized', 'fungible', 'future-proof', 'global', 'go forward', 'goal-oriented', 'granular', 'high standards in', 'high-payoff', 'hyperscale', 'high-quality', 'highly efficient', 'holistic', 'impactful', 'inexpensive', 'innovative', 'installed base', 'integrated', 'interactive', 'interdependent', 'intermandated', 'interoperable', 'intuitive', 'just in time', 'leading-edge', 'leveraged', 'long-term high-impact', 'low-risk high-yield', 'magnetic', 'maintainable', 'market positioning', 'market-driven', 'mission-critical', 'multidisciplinary', 'multifunctional', 'multimedia based', 'next-generation', 'on-demand', 'one-to-one', 'open-source', 'optimal', 'orthogonal', 'out-of-the-box', 'pandemic', 'parallel', 'performance based', 'plug-and-play', 'premier', 'premium', 'principle-centered', 'proactive', 'process-centric', 'professional', 'progressive', 'prospective', 'quality', 'real-time', 'reliable', 'resource-sucking', 'resource-maximizing', 'resource-leveling', 'revolutionary', 'robust', 'scalable', 'seamless', 'stand-alone', 'standardized', 'standards compliant', 'state of the art', 'sticky', 'strategic', 'superior', 'sustainable', 'synergistic', 'tactical', 'team building', 'team driven', 'technically sound', 'timely', 'top-line', 'transparent', 'turnkey', 'ubiquitous', 'unique', 'user-centric', 'user friendly', 'value-added', 'vertical', 'viral', 'virtual', 'visionary', 'web-enabled', 'wireless', 'world-class', 'worldwide']
BS_NOUNS = ['action items', 'alignments', 'applications', 'architectures', 'bandwidth', 'benefits', 'best practices', 'catalysts for change', 'channels', 'clouds', 'collaboration and idea-sharing', 'communities', 'content', 'convergence', 'core competencies', 'customer service', 'data', 'deliverables', 'e-business', 'e-commerce', 'e-markets', 'e-tailers', 'e-services', 'experiences', 'expertise', 'functionalities', 'fungibility', 'growth strategies', 'human capital', 'ideas', 'imperatives', 'infomediaries', 'information', 'infrastructures', 'initiatives', 'innovation', 'intellectual capital', 'interfaces', 'internal or "organic" sources', 'leadership', 'leadership skills', 'manufactured products', 'markets', 'materials', 'meta-services', 'methodologies', 'methods of empowerment', 'metrics', 'mindshare', 'models', 'networks', 'niches', 'niche markets', 'nosql', 'opportunities', '"outside the box" thinking', 'outsourcing', 'paradigms', 'partnerships', 'platforms', 'portals', 'potentialities', 'process improvements', 'processes', 'products', 'quality vectors', 'relationships', 'resources', 'results', 'ROI', 'scenarios', 'schemas', 'services', 'solutions', 'sources', 'strategic theme areas', 'storage', 'supply chains', 'synergy', 'systems', 'technologies', 'technology', 'testing procedures', 'total linkage', 'users', 'value', 'vortals', 'web-readiness', 'web services', 'virtualization']

def bs_txt():
    bs_string  = random.choice(BS_ADVERBS) + ' '
    bs_string += random.choice(BS_VERBS) + ' '
    bs_string  = random.choice(BS_ADJECTIVES) + ' '
    bs_string += random.choice(BS_NOUNS)
    return bs_string

def bs_img():
    cat = random.choice(IMAGE_CAT)
    r = requests.get(IMAGE_URL.format(cat))
    return Image.open(StringIO(r.content))

def main():
    directory = sys.argv[1]
    no_images = int(sys.argv[2])
    img_names = []
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    # download and label images
    for i in range(0, no_images):
        print("Saving image #{0}".format(i))
        text = bs_txt()
        img = bs_img()
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 1280, 100], fill=(255,255,255,70))
        font = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 36)
        draw.text((0, 30), text, (50,50,50), font=font)
        font = ImageFont.truetype('/Library/Fonts/Arial Bold.ttf', 100)
        draw.text((1150, 630), str(i + 1), (255,255,255), font=font)
        name = directory + '/' + '{0}.jpg'.format(i)
        img.save(name)
        img_names.append(name)
    # create pdf from image directory folder
    pdf = FPDF(orientation = 'L')
    pdf.set_auto_page_break(0)
    for image in img_names:
        pdf.add_page()
        pdf.image(image, h=210*0.9, w=297*0.93)
    pdf.output("{0}.pdf".format(directory), "F")

if __name__ == '__main__':
  main()
