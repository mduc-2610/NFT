from math import ceil
import random
import os
from datetime import datetime
from faker import Faker
from PIL import Image
from django.core.management.base import BaseCommand
from NFT.settings import MEDIA_ROOT
from django.contrib.auth.hashers import make_password
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite, \
                                VoteProductComment, VoteBlogComment
fake = Faker()

def run():
    User.objects.all().delete()
    NFTProduct.objects.all().delete()
    Topic.objects.all().delete()
    NFTProductOwner.objects.all().delete()
    Type.objects.all().delete()
    NFTBlog.objects.all().delete()
    BlogSection.objects.all().delete()
    FAQ.objects.all().delete()
    FAQTitle.objects.all().delete()
    ProductComment.objects.all().delete()
    BlogComment.objects.all().delete()
    
    username_superuser = 'duc'
    email_superuser = 'duc@gmail.com'
    password_superuser = 'duc123'

    User.objects.create_superuser(username_superuser, email_superuser, password_superuser)
    print("USER:")
    user_obj_list = []
    for _ in range(30):
        data = {
            "name": fake.email().split('@')[0],
            "email": fake.email().split('@')[0] + '@email.com',
            "username": fake.email().split('@')[0],
            "password": make_password("Duckkucd.123"),
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
        "EtherEssence", "Bitstream", "NFTNocturnes", "CryptoPulse", "DigitalDreams",
        "PixelSculpture", "EtherVisions", "NFTNova", "VirtualCanvas",
        "CryptoKaleidoscope", "BitGallery", "NFTSpectrum", "Decentralized",
        "CyberCanvas", "BlockArt", "MetaMaster", "DigitalAlchemy", "CryptoGraffiti Gems",
        "BitBrush", "PixelMystique", "DecentralArt", "EtherElegance", "NFTInfinite"
    ]
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
    # [print(k, v) for k, v in nft_image_files.items()]

    cnt, z = 1, 0
    nft_product_obj_list = []
    for k, v in nft_image_files.items():
        data={}
        type_product = type_obj_list[z]
        for i, image in enumerate(v):  
            data = {
                "name": nft_names.pop(random.randint(0, len(nft_names) - 1)),
                "price": round(random.uniform(0, 3), 8),
                "rarity": round(random.uniform(0, 0.1), 8),
                "author": random.choice(user_obj_list),
                "image": image,
                "topic": random.choice(topic_obj_list),
                "quantity": random.choice(nft_quantity),
                "description": fake.text(max_nb_chars=300),
                "artwork": cnt,
                "type_product": type_product
            }
            # nft_product_obj, _ = NFTProduct.objects.get_or_create(**data)
            nft_product_obj = NFTProduct.objects.create(**data)
            nft_product_obj_list.append(nft_product_obj)
            print(f"\tSuccesfully created product with info {nft_product_obj.name} {nft_product_obj.price} {nft_product_obj.image} {nft_product_obj.quantity} {nft_product_obj.description} {nft_product_obj.rarity} {nft_product_obj.artwork}")
            cnt += 1
        z += 1

    # Load owner of a nft product
    print("----------------------------------------------------------------")
    print("OWNERS:")
    for user in user_obj_list:
        tmp_list = nft_product_obj_list.copy()
        for i in range(random.randint(0, 25)):
            random_data = tmp_list.pop(random.randint(0, len(tmp_list) - 1))
            data = {
                "user": user,
                "product": random_data
            }
            # nft_product_owner, _ = NFTProductOwner.objects.get_or_create(**data)
            nft_product_owner = NFTProductOwner.objects.create(**data)
            print(f"\tUser with uuid {data['user'].id} owns the nft product with uuid {data['product'].id}")

    # Load who like the product 
    print("----------------------------------------------------------------")
    print("FAVORITES:")
    for user in user_obj_list:
        tmp_list = nft_product_obj_list.copy()
        for i in range(random.randint(0, 15)):
            random_data = tmp_list.pop(random.randint(0, len(tmp_list) - 1))
            data = {
                "user": user,
                "product": random_data
            }
            # nft_product_Favorite, _ = NFTProductFavorite.objects.get_or_create(**data)
            nft_product_Favorite = NFTProductFavorite.objects.create(**data)
            print(f"\tUser with uuid {data['user'].id} likes the nft product with uuid {data['product'].id}")
    

    #Load blog 
    print("----------------------------------------------------------------")
    print("BLOG:")
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
    blog_images, blog_obj_list = [], []
    blog_dir = os.path.join(MEDIA_ROOT, 'blog')
    for file in os.listdir(blog_dir):
        blog_images.append("/static/images/blog/" + file)
    for i in range(len(titles)):
        data = {
            'title': titles[i],
            'author': random.choice(user_obj_list),                
            'image': blog_images[i],
        }
        # blog, _ = NFTBlog.objects.get_or_create(**data)
        blog = NFTBlog.objects.create(**data)
        blog_obj_list.append(blog)
        print(f"\tSuccessfully create blog {blog} {blog.image}")
        num_sections = random.randint(2, 5)
        for _ in range(num_sections):
            data = {
                'image': None,
                'blog': blog,
                'heading': fake.sentence(),
                'content': fake.text(max_nb_chars=5000),
            }
            # blog_section, _ = BlogSection.objects.get_or_create(**data)
            blog_section = BlogSection.objects.create(**data)
            print(f"\t Successfully create blog section {blog_section}")


    print("----------------------------------------------------------------")
    print("FAQs:")
    faqs = {
        'Collectors': [
            {'Creating a MetaMask Wallet in Five Steps':
             '''Install MetaMask, set up a wallet with a strong password and save your seed phrase.
Fund your wallet with cryptocurrency.
Explore the wallet's features and interface.
Prioritize security to protect your assets.
'''
             },
            {'Meecat Drops: Collectibles Information Tooltips':'''Meecat Drops provides tooltips with information about collectibles, including rarity and metadata, enhancing the user experience.'''},
            {'Storing, Displaying and Transferring NFTs':'''
Choose a compatible wallet for your NFTs.
Connect the wallet to a marketplace.
View, transfer, and display your NFTs securely.
'''},
            {'A Guide to Buying Digital Collectibles':'''Research digital collectibles and creators.
Choose a reputable marketplace.
Set up a cryptocurrency wallet.
Bid, buy, and transfer NFTs.
Display and stay informed about your collectibles.'''},
            {'Creating a MetaMask Wallet in Five Steps':'''
Install MetaMask, set up a wallet with a strong password and save your seed phrase.
Fund your wallet with cryptocurrency.
Explore the wallet's features and interface.
Prioritize security to protect your assets.
'''},
            {'Fixed Price and Offer-based Listings':'''Fixed price listings have a set price for NFTs.
Offer-based listings allow buyers to make offers, with potential negotiation between the seller and buyer.'''}
        ],
        'General': [
            {'Platform Commission and Secondary Market Sales and Royalties':'''This topic likely covers the fees that a platform charges for hosting and facilitating NFT sales. It may also explain how secondary market sales work and how royalties are distributed to creators when their NFTs are resold.'''},
            {'Meecat Drops: Collectibles Information Tooltips':'''This topic discusses "Meecat Drops," a feature that provides informational tooltips about collectible items, improving the user experience for those exploring collectibles.'''},
            {'\'Meecat\'s Token Standard: ERC-1155':'''This topic is likely about Meecat's use of the ERC-1155 token standard, which is a common standard on the Ethereum blockchain for creating both fungible and non-fungible tokens (NFTs).'''},
            {'Returns, Delivery Costs and Additional Charges':'''This likely covers the policies and costs associated with returning NFTs or digital collectibles, as well as any additional fees or charges that buyers may encounter.'''},
            {'Creating and Curating a Collection':'''This topic may explain how users can create and curate their own collections of NFTs, which can be a valuable aspect of the NFT ecosystem for collectors and creators alike.'''},
            {'The Meecat Duck Membership System:':'''This topic likely delves into the "Meecat Duck Membership System," which could be a loyalty or rewards program offered by the platform, possibly providing special benefits or access to members.'''}
        ],
        'Artists': [
            {'Listing NFT Artworks':'''This topic likely explains the process and steps involved in listing NFT artworks on the Dissrup marketplace, covering how creators can showcase and sell their digital art as NFTs.'''},
            {'Technical Specifications for Uploading Artwork to the Dissrup Marketplace':'''This topic likely provides technical guidelines and requirements for artists and creators to follow when uploading their artwork to the Dissrup marketplace. It may include details on file formats, resolutions, and other specifications.'''},
            {'Crypto Transaction Fees Explained':'''This topic is likely a guide that clarifies the various fees associated with cryptocurrency transactions, particularly as they relate to buying, selling, or trading NFTs on the Dissrup platform. It may cover aspects like gas fees and transaction processing costs.'''},
            {'Joining Dissrup as a Creator':'''This topic likely outlines the process for artists and creators to become part of the Dissrup platform as content creators. It may include information on how to register, set up a profile, and start listing their creations as NFTs for sale.'''}
        ],
        'Enjin': [
            {'How long does it take to integrate NFTs with my app?':'''The time required to integrate NFTs with your app can vary depending on your project's complexity and your development team's expertise. Enjin provides tools and resources to streamline the process, but the exact timeline can differ from project to project.'''},
            {'Is the Enjin Platform free to use?':'''Enjin offers a range of tools and services, some of which are free, while others may have associated costs. The specific pricing and availability of free features may change, so it's advisable to check Enjin's official website or documentation for the most up-to-date information.'''},
            {'Is there a developer community I can join?':'''Yes, Enjin has an active developer community where you can connect with other developers, share knowledge, and collaborate on projects. Joining this community can be valuable for getting support and staying updated on Enjin-related developments.'''},
            {'Why is every NFT backed with Enjin Coin?':'''Enjin Coin (ENJ) is often used as a backing mechanism for NFTs on the Enjin platform to provide real-world value and scarcity to digital assets. It can be used to determine the value and authenticity of NFTs, as each NFT is linked to a quantity of ENJ, which can be redeemed or melted to claim the underlying assets.'''},
            {'Do I need to know how to code to create NFTs?':'''While some knowledge of coding may be helpful for advanced customization, Enjin's platform is designed to be user-friendly, allowing individuals with varying levels of technical expertise to create NFTs without extensive coding skills. You can use Enjin's tools and templates to mint NFTs with relative ease.'''}
        ]
    }
    
    for title, questions in faqs.items():
        data = {
            'title': title
        }
        # faq_title, _ = FAQTitle.objects.get_or_create(title)
        faq_title = FAQTitle.objects.create(**data)
        print(f"\tSuccessfully created FAQ title {faq_title.title}")
        for question in questions:
            for k, v in question.items():
                data = {
                    'title': faq_title,
                    'question': k,
                    'answer': v,
                }
                # faq, _ = FAQ.objects.get_or_create(**data)
                faq = FAQ.objects.create(**data)
                print(f"\tSuccessfully created FAQ question {faq.question} with answer {faq.answer}")
                
    # Load random data product comment
    print("----------------------------------------------------------------")
    print("PRODUCT COMMENT:")
    product_comment_list = []
    for product in nft_product_obj_list:
        tmp_user = user_obj_list.copy()
        for _ in range(random.randint(1, 10)):  # You can adjust the range as needed
            data = {
                "user": tmp_user.pop(random.randint(0, len(tmp_user) - 1)),
                "product": product,
                "content": fake.text(max_nb_chars=random.randint(100, 750))
            }
            # product_comment, _ = ProductComment.objects.get_or_create(product_comment)
            product_comment = ProductComment.objects.create(**data)
            product_comment_list.append(product_comment)
            print(f"\t Successfully create Product Comment {product_comment.product.name} {product_comment.user.name} ")
            
    # Load ramdom user like product comment
    print("----------------------------------------------------------------")
    print("RANDOM USER LIKE PRODUCT COMMENT:")
    for user in user_obj_list:
        tmp_list = product_comment_list.copy()
        for i in range(random.randint(0, 20)):
            random_data = tmp_list.pop(random.randint(0, len(tmp_list) - 1))
            data = {
                "user": user,
                "comment": random_data
            }
            # product_comment_vote, _ = VoteProductComment.objects.get_or_create(**data)
            product_comment_vote = VoteProductComment.objects.create(**data)
            print(f"\tUser with uuid {data['user'].id} likes the product comment with uuid {data['comment'].id}")
    
    # Load random data blog comment
    print("----------------------------------------------------------------")
    print("BLOG COMMENT:")
    blog_comment_list = []
    for blog in blog_obj_list:
        tmp_user = user_obj_list.copy()
        for _ in range(random.randint(1, 10)):  # You can adjust the range as needed
            data = {
                "user": tmp_user.pop(random.randint(0, len(tmp_user) - 1)),
                "blog": blog,
                "content": fake.text(max_nb_chars=random.randint(300, 750)),
            } 
            # blog_comment, _ = BlogComment.objects.get_or_create(blog_comment)
            blog_comment = BlogComment.objects.create(**data)
            blog_comment_list.append(blog_comment)
            print(f"\t Successfully create Blog Comment {blog_comment.blog.title} {blog_comment.user.name} ")

    # Load ramdom user like blog comment
    print("----------------------------------------------------------------")
    print("RANDOM USER LIKE BLOG COMMENT:")
    for user in user_obj_list:
        tmp_list = blog_comment_list.copy()
        for i in range(random.randint(0, 20)):
            random_data = tmp_list.pop(random.randint(0, len(tmp_list) - 1))
            data = {
                "user": user,
                "comment": random_data
            }
            # blog_comment_vote, _ = VoteBlogComment.objects.get_or_create(**data)
            blog_comment_vote = VoteBlogComment.objects.create(**data)
            print(f"\tUser with uuid {data['user'].id} likes the blog comment with uuid {data['comment'].id}")
    