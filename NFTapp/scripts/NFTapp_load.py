from math import ceil
import random
import os
from datetime import datetime
from faker import Faker
from PIL import Image
from django.core.management.base import BaseCommand
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Type, NFTBlog, Comment, BlogSection
from NFT.settings import MEDIA_ROOT
fake = Faker()

def run():
    User.objects.all().delete()
    NFTProduct.objects.all().delete()
    Topic.objects.all().delete()
    OwnerNFTProduct.objects.all().delete()
    Type.objects.all().delete()
    NFTBlog.objects.all().delete()
    Comment.objects.all().delete()
    BlogSection.objects.all().delete()

    username_superuser = 'duc'
    email_superuser = 'duc@fgmail.com'
    password_superuser = 'duc123'

    User.objects.create_superuser(username_superuser, email_superuser, password_superuser)
    print("USER:")
    user_obj_list = []
    for _ in range(30):
            data = {
                "name": fake.email().split('@')[0],
                "email": fake.email(),
                "username": fake.email().split('@')[0],
                "password":fake.password(),
                "bio": fake.text(max_nb_chars=300),
            }
            # user, _ = User.objects.get_or_create(**data)
            user = User.objects.create(**data)
            print(f"\tSuccessfully created user with info {user.name}, {user.email}, {user.bio} ")
            user_obj_list.append(user)

    # Load type obj
    print("----------------------------------------------------------------")
    print("TYPE:")
    types = ['artworks', 'collections']
    type_obj_list = []
    for type in types:
        data = {
            "name": type
        }
        # type_obj, _ = Type.objects.get_or_create(**data)
        type_obj = Type.objects.create(**data)
        type_obj_list.append(type_obj)
        print(f"\tSuccesfully created type {type}")

    # Load topic obj
    print("----------------------------------------------------------------")
    print("TOPIC:")
    topics = ['Alternate Medium Space', 'KittyMotions', 'Digital Fashion World']
    topic_obj_list = []
    for topic in topics:
        data = {
            "name": topic
        }
        # topic_obj, _ = Topic.objects.get_or_create(**data)
        topic_obj = Topic.objects.create(**data)
        topic_obj_list.append(topic_obj)
        print(f"\tSuccesfully created topic {topic}")

    # Load author obj
    # print("----------------------------------------------------------------")
    # print("AUTHOR:")
    # authors = [user.name for user in User.objects.all() if user.creator]
    # author_obj_list = []
    # for author in authors:
    #     data = {
    #         "name": author
    #     }
    #     # author_obj, _ = Author.objects.get_or_create(**data)
    #     author_obj = Author.objects.create(**data)
    #     author_obj_list.append(author_obj)
    #     print(f"\tSuccesfully created author {author}")

    # Load nft product
    print("----------------------------------------------------------------")
    print("Product:")
    nft_names = [
        "EtherGems", "CryptoCanvas", "DigitalDreamscapes", "PixelPioneers", "CryptoCollectibles", 
        "ArtBlockChain", "NFTNova", "DecentralizedVisions", "VirtualVogue", "TechnoTreasuries", 
        "MetaMasterpieces", "BitArtGallery", "EtherIcons", "NeonNomads", "CryptoCraftworks", "NFTUniverse", 
        "DigitalDynasty", "BlockchainBrushstrokes", "PixelPrestige", "EtherEnigmas", "CodeCanvas", 
        "CryptoChronicles", "VirtualVagabonds", "BitBliss", "NFTNirvana", "ArtisticAlgorithms", "CryptoCuriosities", 
        "EtherEssence", "BitstreamBoulevard", "NFTNocturnes"
    ]
    nft_prices = [round(random.uniform(0, 10), 2) for _ in range(30)]
    nft_quantity = [random.randint(0, 20) for _ in range(30)]
    nft_image_files = {}
    explore_dir = os.path.join(MEDIA_ROOT, "explore")
    for dir in os.listdir(explore_dir):
        inside_dir = os.path.join(explore_dir, dir)
        path = "/static/images/explore/" + dir + "/"
        nft_image_files.update({dir: []})
        for file in os.listdir(inside_dir):
            print(path)
            nft_image_files[dir].append(path + file)
    [print(k, v) for k, v in nft_image_files.items()]

    cnt = 1
    nft_product_obj_list = []
    for k, v in nft_image_files.items():
        data={}
        if k.startswith("collection"):
            data.update({"type": type_obj_list[0]})
        else: 
            cnt = 1
            data.update({"type": type_obj_list[1]})
        for image in v:  
            data = {
                "name": random.choice(nft_names),
                "price": random.choice(nft_prices),
                "author": random.choice(user_obj_list),
                "image": image,
                "topic": random.choice(topic_obj_list),
                "quantity": random.choice(nft_quantity),
                "description": fake.text(max_nb_chars=300),
                "stars": random.randint(0, 5),
                "artwork": cnt
            }
            # nft_product_obj, _ = NFTProduct.objects.get_or_create(**data)
            nft_product_obj = NFTProduct.objects.create(**data)
            nft_product_obj_list.append(nft_product_obj)
            print(f"\tSuccesfully created product with info {nft_product_obj.name} {nft_product_obj.price} {nft_product_obj.image} {nft_product_obj.quantity} {nft_product_obj.description} {nft_product_obj.stars} {nft_product_obj.artwork}")
            cnt += 1

    # Load owner of a nft product
    print("----------------------------------------------------------------")
    for user in user_obj_list:
        for i in range(random.randint(3, 5)):
            data = {
                "owner": user,
                "product": random.choice(nft_product_obj_list)
            }
            # owner_nft_product, _ = OwnerNFTProduct.objects.get_or_create(**data)
            owner_nft_product = OwnerNFTProduct.objects.create(**data)
            print(f"\tUser with uuid {data['owner'].id} owns the nft product with uuid {data['product'].id}")

    #Load blog 
    print("----------------------------------------------------------------")
    titles = [
        'Awesome NFT Projects That Aren’t PFP Collections',
        'Sloooths: How NFT Art Can Help Mental Health',
        'Big Hugs Studio: Minting Their First NFT Project With',
        'Chia Friends: From Network to Collection',
        'Urban Animals NFT: Una Nueva Era Ha Comenzado',
        'Scaling Your NFT Project: A Beginner’s Guide to IPFS',
        'Token Gating: Creating Exclusivity in the Metaverse',
        '5 Essential Tools for NFT Creators',
        'NFT Twitter Spaces You Should Listen to in 2022',
        'What Are NFT Airdrops and Why Do They Matter?',
        'Why NFT Projects Need Utility',
        'Serwah Attafuah and Glitch of Mind Talk Afrofuturism',
        'Awesome NFT Projects That Aren’t PFP Collections',
        'The Moral Complexity of Ethics in NFTs',
        'Integrates Pinata to Provide Creators with IPFS Upload'
    ]
    blog_images = []
    blog_dir = os.path.join(MEDIA_ROOT, 'blog')
    for file in os.listdir(blog_dir):
        blog_images.append("/static/images/blog/" + file)
    for i in range(len(titles)):
        blog = NFTBlog.objects.create(
            title=titles[i],
            author=random.choice(user_obj_list),                
            image=blog_images[i],
        )
        print(f"\tSuccessfully create blog {blog} {blog.image}")
        num_sections = random.randint(2, 5)
        for _ in range(num_sections):
            blog_section = BlogSection.objects.create(
                image=None,
                blog=blog,
                heading=fake.sentence(),
                content=fake.text(max_nb_chars=5000),
            )
            print(f"\t\t Successfully create blog section {blog_section}")
    
