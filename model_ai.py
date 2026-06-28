import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO
import json

load_dotenv()


def set_openai_api_key(api_key):
    """Set the OpenAI key for the current app session."""
    clean_key = api_key.strip() if api_key else ""
    if not clean_key:
        raise ValueError("OpenAI API key is required.")

    os.environ["OPENAI_API_KEY"] = clean_key
    openai.api_key = clean_key


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please enter your OpenAI API key before using VisAI.")

    return OpenAI(api_key=api_key)


def verify_image_url(url):
    """Verify if URL contains a valid, accessible image"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return False

        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return False

        Image.open(BytesIO(response.content))
        return True
    except Exception:
        return False


def get_response(prompt):
    response = get_openai_client().chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt,
        temperature=0
    )

    return response


def generate_prompt(list_image_urls):
    if not list_image_urls:
        return {
            "case": "Need Further Verification",
            "reason": "No Images Found In This Purchase Order",
            "total_token": 0
        }

    verified_urls = [url for url in list_image_urls if verify_image_url(url)]

    if not verified_urls:
        return {
            "case": "Need Further Verification",
            "reason": "Image is Invalid",
            "total_token": 0
        }

    prompt = [
        {
            "role": "system",
            "content": """You are an expert involves assessing product defects by analyzing provided list of product images and related data. You will be provided with a list of product images. Based on the information provided, analyze the situation and determine whether the defect in the product was caused by the vendor or the carriers.

            Our Category Product: Arts Crafts & Sewing, Baby Products, Bags, Wallets and Luggage, Beauty & Personal Care, Clothing Shoes & Jewelry, Electronics, Health & Household, Home & Kitchen, Home Improvement, Industrial & Scientific, Office Products, Patio, Lawn & Garden, Pet Supplies, Replacement, Sports & Outdoors, Tools & Home Improvement, Toys & Game, WH Supply. (Sửa Category Product).

            Case 'Vendors' means that the vendor causes the defect (Vendor is responsible for producing, processing, and packaging goods or components. Their operations ensure products are ready for distribution to intermediaries or direct sales to end consumers. They must ensure that package and the product box are intact before sending it to the carrier)
            1. If the list of images does not include the box, package, carton, etc. Then check product or part of the product is broken, missing, defective, not fully assembled, dented, chip, convex, rust, bump, crack, damaged, good in condition, intact, not align ed, missing screw hole, bent, warp, misalignment, painted hair, missing parts. In this case, you need to analyze in depth whether the product is damaged due to carriers or vendors.
            2. If the product is defective, incorrect size, or missing due to Vendor.
            3. If the product is not working as normal product, or the joints are not machined accurately.
            4. The product or parts of it are described using keywords such as: 'Broken', 'Cracked', 'Chipped', 'Dented', 'Scratched', 'Convex', 'Bumped', 'Bent', 'Warped', 'Rusty', 'Tarnished', 'Peeling', 'Faded', 'Missing part', 'Missing screw hole', 'Missing hardware', 'Incomplete assembly', 'Not aligned', 'Misalignment', 'Uneven gaps', 'Improper fit', 'Offset placement', 'Discolored', 'Stains', 'Sticky surface', 'Rough finish', 'Used', 'Scratched', 'Scuffed', 'Peeled paint', 'Bubbled paint', 'Discolored', 'Stained', 'Faded', 'Polished unevenly', 'Uneven edges', 'Wavy surface', 'Pitted surface', 'Bumpy texture', 'Deformed appearance', 'Dull finish', 'Uneven coating', 'Matte instead of glossy', 'Chipped coating', 'Over-sprayed paint', 'Cracked surface', 'Warped surface', 'Melted edge', 'Softened material', 'Brittle material', 'Rough finish', 'Sticky surface', 'Greasy feel', 'Uneven texture', 'Chalky surface', 'Misaligned seams', 'Gaps in assembly', 'Visible glue', 'Protruding screws', 'Excess material', 'Dusty surface', 'Scratched during transit', 'Markings from packaging', 'Loose parts', 'Stiff movement', 'Frozen mechanism', 'Misaligned movement', 'Uneven operation', 'Noisy mechanism', 'Underperforming', 'Inconsistent output', 'Slow response', 'Overheating', 'Low efficiency', 'Unstable performance', 'Incorrect fit', 'Wobbling assembly', 'Improper fastening', 'Gaps in assembly', 'Missing alignment', 'Missing accessories', 'Non-functional accessory', 'Misfitting parts', 'Damaged components'. It is because the vendor damaged the product.

            Case 'Carriers': means that the defect was caused by the carriers (Carriers is shipping provider is critical in the supply chain, facilitating the seamless transfer of orders from the seller's warehouse to the end customer. Their efficiency ensures timely delivery, shipment integrity, and accurate tracking, directly influencing fulfillment performance and customer satisfaction.):
            1. There are images of damaged boxes or packaging materials provided by the customer. If in a list of images have the box, package, carton, etc. box, packaging material (foam, cardboard, strap, poly bag, handling labels, shrink wrap): torn, damaged, broken, hole, beaten, wrong label, different brand, wet, wrinkled. This is because the carrier damaged the product.
            2. If there is more than one image. If just need one image of the box and packaging material is broken then the carrier damaged the product.
            3. If the product is damaged during the shipping process, the damage is described using keywords such as: 'Box crushed during transit', 'Box ripped apart', 'Box sides collapsed', 'Box with torn flaps', 'Box with exposed content', 'Box punctured', 'Box deformed', 'Box with missing seals', 'Box partially opened', 'Torn packaging material', 'Damaged foam','Wet foam', 'Broken strap', 'Loose strap', 'Missing strap', 'Torn poly bag', 'Wet poly bag', 'Missing poly bag', 'Shrink wrap torn', 'Shrink wrap missing', 'Wrong handling label','Missing handling label', 'Foam damaged on edges', 'Foam compressed beyond use','Bubble wrap burst', 'Loose packing materials','Cardboard insert torn or missing', 'Poly bag punctured','Shrink wrap loosely applied', 'Shrink wrap completely removed', 'Strapping improperly applied', 'Strapping cut during handling', 'Labels placed incorrectly (e.g., covering warnings)','Handling instructions label torn','Packaging exposed to water','Packaging soaked','Packaging with mud stains','Packaging faded from sunlight exposure', 'Packaging with oil or grease stains', 'Packaging crushed by stacking', 'Overloaded boxes causing stress on materials', 'Mishandling during transit (e.g., dropped box)', 'Failure to secure packaging on pallets', 'Packaging damaged by forklifts or conveyor belts', 'Missing packaging material (e.g., void fill not included)', 'Misaligned box flaps or seals', 'Packaging material swapped without authorization', 'Product exposed due to insufficient padding','Tampered box seals'. It is because the carrier damaged the product.

            Case 'Need Further Verification': Use this only if the provided images do not match the criteria for 'Vendors' or 'Carriers'. You must priority case 'Vendors' or 'Carriers'. This should be the least likely response and used only as a fallback"
            
            Your response should only state 'Vendors' or 'Carriers' or 'Need Further Verification' to know who is responsible for the damaged based on the list of images?  Explain why, how, describe you chose this case like a expert in this situation? You don't explain how your logic works.
            
            Flow Process:
            1. Check Case 'Vendors' and get result
            2. Check Case 'Carriers' and get result
            3. After that compare result to get final result
            
            Always return the output as a **raw JSON object** without additional formatting, such as backticks or annotations.
            Output format:
            {
                "case": "Vendors" or "Carriers" or "Need Further Verification",
                "reason": "reason"
            }
            """,
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Based on this list images. Help me check Who is responsible for the damaged?"},
            ] + [{"type": "image_url", "image_url": {"url": url}} for url in list_image_urls]
        }
    ]

    # Call the OpenAI to get the response
    result = get_response(prompt)

    # Total token spent
    total_token = result.usage.total_tokens

    # Get the content
    content = result.choices[0].message.content

    # Parse the content
    response = json.loads(content)

    # Add the total token
    response['total_token'] = total_token

    return response


# if __name__ == "__main__":
#     # Vendors
#     list_image_urls = [
#         "https://assets.wfcdn.com/im/27981540/compr-r85/2846/284679600/default_image.jpg",
#         "https://assets.wfcdn.com/im/11771640/compr-r85/2846/284679596/default_image.jpg",
#         "https://assets.wfcdn.com/im/65154718/compr-r85/2846/284679547/default_image.jpg",
#         "https://assets.wfcdn.com/im/00654390/compr-r85/2846/284679594/default_image.jpg",
#         "https://assets.wfcdn.com/im/77577085/compr-r85/2846/284679601/default_image.jpg"
#     ]

    # Carriers
    # list_image_urls = [
    #     "https://assets.wfcdn.com/im/82511021/compr-r85/2926/292654294/default_image.jpg",
    #     "https://assets.wfcdn.com/im/76952396/compr-r85/2926/292654295/default_image.jpg"
    # ]

    # Vendors
    # list_image_urls = [
    #     "https://assets.wfcdn.com/im/65498728/compr-r85/2974/297470665/default_image.jpg",
    #     "https://assets.wfcdn.com/im/79245092/compr-r85/2987/298780233/default_image.jpg",
    #     "https://assets.wfcdn.com/im/20303389/compr-r85/2987/298780281/default_image.jpg",
    #     "https://assets.wfcdn.com/im/35557681/compr-r85/2974/297470619/default_image.jpg",
    #     "https://assets.wfcdn.com/im/10058585/compr-r85/2987/298780269/default_image.jpg",
    #     "https://assets.wfcdn.com/im/89922263/compr-r85/2987/298780249/default_image.jpg",
    #     "https://assets.wfcdn.com/im/25482200/compr-r85/2974/297470643/default_image.jpg",
    #     "https://assets.wfcdn.com/im/97493224/compr-r85/2987/298780259/default_image.jpg",
    #     "https://assets.wfcdn.com/im/97053145/compr-r85/2987/298780225/default_image.jpg"
    # ]

    # Vendors
    # list_image_urls = [
    #     "https://assets.wfcdn.com/im/27981540/compr-r85/2846/284679600/default_image.jpg",
    #     "https://assets.wfcdn.com/im/11771640/compr-r85/2846/284679596/default_image.jpg",
    #     "https://assets.wfcdn.com/im/65154718/compr-r85/2846/284679547/default_image.jpg",
    #     "https://assets.wfcdn.com/im/00654390/compr-r85/2846/284679594/default_image.jpg",
    #     "https://assets.wfcdn.com/im/77577085/compr-r85/2846/284679601/default_image.jpg"
    # ]

    # Need Further Verification
    # list_image_urls = [
    #     "https://assets.wfcdn.com/im/87476811/compr-r85/2876/287618672/default_image.jpg",
    #     "https://assets.wfcdn.com/im/98594061/compr-r85/2876/287618670/default_image.jpg",
    #     "https://assets.wfcdn.com/im/93035436/compr-r85/2876/287618671/default_image.jpg",
    #     "https://assets.wfcdn.com/im/64018077/compr-r85/2876/287618669/default_image.jpg",
    #     "https://assets.wfcdn.com/im/35724413/compr-r85/2883/288396386/default_image.jpg",
    #     "https://assets.wfcdn.com/im/76102051/compr-r85/2883/288396391/default_image.jpg",
    #     "https://assets.wfcdn.com/im/90934827/compr-r85/2876/287608486/default_image.jpg"
    # ]

    # response = generate_prompt(list_image_urls)

    # print(response)
