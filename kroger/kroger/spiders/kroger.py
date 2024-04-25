import math
from urllib.parse import urljoin
import scrapy


class KrogerSpider(scrapy.Spider):
    name = 'kroger'
    allowed_domains = ['x']
    start_urls = ['https://www.kroger.com/pl/fresh-fruit/06111?pzn=relevance',
 'https://www.kroger.com/pl/fresh-vegetables/06112?pzn=relevance',
 'https://www.kroger.com/pl/fresh-herbs/06122?pzn=relevance',
 'https://www.kroger.com/pl/salads/06114?pzn=relevance',
 'https://www.kroger.com/pl/dressings-dips/06110?pzn=relevance',
 'https://www.kroger.com/pl/fresh-cut-fruit-vegetables/06121?pzn=relevance',
 'https://www.kroger.com/pl/packaged-produce/06123?pzn=relevance',
 'https://www.kroger.com/pl/party-trays/06119?pzn=relevance',
 'https://www.kroger.com/pl/fresh-juice-smoothies/06113?pzn=relevance',
 'https://www.kroger.com/pl/beef/05001?pzn=relevance',
 'https://www.kroger.com/pl/chicken/05002?pzn=relevance',
 'https://www.kroger.com/pl/pork-ham/05006?pzn=relevance',
 'https://www.kroger.com/pl/turkey/05012?pzn=relevance',
 'https://www.kroger.com/pl/lamb-veal-bison/05014?pzn=relevance',
 'https://www.kroger.com/pl/specialty-meat/05011?pzn=relevance',
 'https://www.kroger.com/pl/bacon-breakfast-sausage/05017?pzn=relevance',
 'https://www.kroger.com/pl/packaged-deli-meat/05013?pzn=relevance',
 'https://www.kroger.com/pl/dinner-sausage/05003?pzn=relevance',
 'https://www.kroger.com/pl/heat-serve-meals-and-sides/05016?pzn=relevance',
 'https://www.kroger.com/pl/hot-dogs-franks/05005?pzn=relevance',
 'https://www.kroger.com/pl/pepperoni-salami-summer-sausage/05015?pzn=relevance',
 'https://www.kroger.com/pl/lunch-snack-kits/05018?pzn=relevance',
 'https://www.kroger.com/pl/canned-meat/0100600006?pzn=relevance',
 'https://www.kroger.com/pl/refrigerated-pickles-sauerkraut/05008?pzn=relevance',
 'https://www.kroger.com/pl/frozen-meat-alternatives/1900800005?pzn=relevance',
 'https://www.kroger.com/pl/shrimp/0501000009?pzn=relevance',
 'https://www.kroger.com/pl/frozen-fish/1900800003?pzn=relevance',
 'https://www.kroger.com/pl/seafood-salads-dips/0500400020?pzn=relevance',
 'https://www.kroger.com/pl/canned-seafood/0100600007?pzn=relevance',
 'https://www.kroger.com/pl/seasonings-sauces/05009?facets=true?pzn=relevance',
 'https://www.kroger.com/pl/sushi/1300800002?pzn=relevance',
 'https://www.kroger.com/pl/fresh-deli-meats/13001?pzn=relevance',
 'https://www.kroger.com/pl/fresh-deli-cheese/13002?pzn=relevance',
 'https://www.kroger.com/pl/hot-meals/13007?pzn=relevance',
 'https://www.kroger.com/pl/specialty-cheeses/13005?pzn=relevance',
 'https://www.kroger.com/pl/olives-dips-spreads-snacks/13011?pzn=relevance',
 'https://www.kroger.com/pl/packaged-deli-meat/13003?pzn=relevance',
 'https://www.kroger.com/pl/packaged-deli-cheese/13004?pzn=relevance',
 'https://www.kroger.com/pl/ready-to-heat-meals/13006?pzn=relevance',
 'https://www.kroger.com/pl/cold-side-dishes/13009?pzn=relevance',
 'https://www.kroger.com/pl/grab-go-meals/13008?pzn=relevance',
 'https://www.kroger.com/pl/party-platters/13010?pzn=relevance',
 'https://www.kroger.com/pl/cakes-cupcakes/14163?pzn=relevance',
 'https://www.kroger.com/pl/donuts-danishes-muffins/14166?pzn=relevance',
 'https://www.kroger.com/pl/cookies-brownies/14165?pzn=relevance',
 'https://www.kroger.com/pl/pies/14169?pzn=relevance',
 'https://www.kroger.com/pl/angel-food-pound-pudding-cakes/14161?pzn=relevance',
 'https://www.kroger.com/pl/cheesecakes/14164?pzn=relevance',
 'https://www.kroger.com/pl/sweet-goods-snacks/14180?pzn=relevance',
 'https://www.kroger.com/pl/artisan-breads/14162?pzn=relevance',
 'https://www.kroger.com/pl/buns/1416700656?pzn=relevance',
 'https://www.kroger.com/pl/packaged-breads/14167?pzn=relevance',
 'https://www.kroger.com/pl/pizza-crust-breadsticks/14171?pzn=relevance',
 'https://www.kroger.com/pl/pita-flat-breads-wraps/14170?pzn=relevance',
 'https://www.kroger.com/pl/fresh-cut-roses/09130?pzn=relevance',
 'https://www.kroger.com/pl/bouquets/09126?pzn=relevance',
 'https://www.kroger.com/pl/floral-arrangements/09128?pzn=relevance',
 'https://www.kroger.com/pl/ferns-outdoor-floral/09127?pzn=relevance',
 'https://www.kroger.com/pl/potted-plants/09133?pzn=relevance',
 'https://www.kroger.com/pl/orchids/09132?pzn=relevance',
 'https://www.kroger.com/pl/packaged-bread/01016?pzn=relevance',
 'https://www.kroger.com/pl/canned-foods/01006?pzn=relevance',
 'https://www.kroger.com/pl/baking-cooking/01012?pzn=relevance',
 'https://www.kroger.com/pl/condiments-sauces/01008?pzn=relevance',
 'https://www.kroger.com/pl/pasta-pasta-sauces/01010?pzn=relevance',
 'https://www.kroger.com/pl/grains-beans-rice/01007?pzn=relevance',
 'https://www.kroger.com/pl/packaged-meals-sides/01011?pzn=relevance',
 'https://www.kroger.com/pl/spreads-jelly-honey/01014?pzn=relevance',
 'https://www.kroger.com/pl/spices-seasonings/01015?pzn=relevance',
 'https://www.kroger.com/pl/indian-foods/0101300170?pzn=relevance',
 'https://www.kroger.com/pl/european-foods/0101300166?pzn=relevance',
 'https://www.kroger.com/pl/kosher-foods/0101300004?pzn=relevance',
 'https://www.kroger.com/pl/milk-plant-based-%20milk/02001?pzn=relevance',
 'https://www.kroger.com/pl/cream-creamer/02005?pzn=relevance',
 'https://www.kroger.com/pl/eggs-egg-substitutes/02003?pzn=relevance',
 'https://www.kroger.com/pl/cheese/02002?pzn=relevance',
 'https://www.kroger.com/pl/yogurt/02009?pzn=relevance',
 'https://www.kroger.com/pl/butter-margarine/02004?pzn=relevance',
 'https://www.kroger.com/pl/sour-cream-dips/02006?pzn=relevance',
 'https://www.kroger.com/pl/refrigerated-dough-crust/02007?pzn=relevance',
 'https://www.kroger.com/pl/pudding-gelatin/02008?pzn=relevance',
 'https://www.kroger.com/pl/frozen-pizza/19003?pzn=relevance',
 'https://www.kroger.com/pl/frozen-meals-sides/19004?pzn=relevance',
 'https://www.kroger.com/pl/frozen-appetizers-snacks/19006?pzn=relevance',
 'https://www.kroger.com/pl/frozen-breakfast/19007?pzn=relevance',
 'https://www.kroger.com/pl/frozen-potatoes-onion-rings/19010?pzn=relevance',
 'https://www.kroger.com/pl/international-frozen-foods/19013?pzn=relevance',
 'https://www.kroger.com/pl/frozen-meat-seafood-meatless/19008?pzn=relevance',
 'https://www.kroger.com/pl/frozen-bread/19009?pzn=relevance',
 'https://www.kroger.com/pl/ice-cream-ice-pops/19002?pzn=relevance',
 'https://www.kroger.com/pl/frozen-desserts/19001?pzn=relevance',
 'https://www.kroger.com/pl/frozen-vegetables/19005?pzn=relevance',
 'https://www.kroger.com/pl/frozen-fruit/19012?pzn=relevance',
 'https://www.kroger.com/pl/frozen-juice-mixers/19011?pzn=relevance',
 'https://www.kroger.com/pl/ice/19014?pzn=relevance',
 'https://www.kroger.com/pl/organic-produce/18003?pzn=relevance',
 'https://www.kroger.com/pl/meat-seafood/18004?pzn=relevance',
 'https://www.kroger.com/pl/dairy-eggs/18007?pzn=relevance',
 'https://www.kroger.com/pl/bakery-bread/18009?pzn=relevance',
 'https://www.kroger.com/pl/deli/18008?pzn=relevance',
 'https://www.kroger.com/pl/grocery/18012?pzn=relevance',
 'https://www.kroger.com/pl/frozen/18010?pzn=relevance',
 'https://www.kroger.com/pl/beverages/18005?pzn=relevance',
 'https://www.kroger.com/pl/spices-baking/18006?pzn=relevance',
 'https://www.kroger.com/pl/cleaning-household/18011?pzn=relevance',
 'https://www.kroger.com/pl/beauty-personal-care/18001?pzn=relevance',
 'https://www.kroger.com/pl/baby/18002?pzn=relevance',
 'https://www.kroger.com/pl/soda-pop/04001?pzn=relevance',
 'https://www.kroger.com/pl/juice/04004?pzn=relevance',
 'https://www.kroger.com/pl/drink-boxes-pouches/04010?pzn=relevance',
 'https://www.kroger.com/pl/sports-energy-drinks/04005?pzn=relevance',
 'https://www.kroger.com/pl/drink-mixes-beverage-enhancers/04008?pzn=relevance',
 'https://www.kroger.com/pl/water/04006?pzn=relevance',
 'https://www.kroger.com/pl/sparkling-water/04002?pzn=relevance',
 'https://www.kroger.com/pl/coffee/04003?pzn=relevance',
 'https://www.kroger.com/pl/tea-kombucha/04007?pzn=relevance',
 'https://www.kroger.com/pl/cereal-granola/03001?pzn=relevance',
 'https://www.kroger.com/pl/breakfast-cereal-bars/03002?pzn=relevance',
 'https://www.kroger.com/pl/bread-bagels-muffins/03004?pzn=relevance',
 'https://www.kroger.com/pl/donuts-pastries/03005?pzn=relevance',
 'https://www.kroger.com/pl/pancake-waffle-baking-mixes/03003?pzn=relevance',
 'https://www.kroger.com/pl/dairy-refrigerated-breakfast/03006?pzn=relevance',
 'https://www.kroger.com/pl/bacon-sausage/05017?pzn=relevance',
 'https://www.kroger.com/pl/juice-breakfast-drinks/03007?pzn=relevance',
 'https://www.kroger.com/pl/chocolate/23001?pzn=relevance',
 'https://www.kroger.com/pl/gummy-chewy-candy/23003?pzn=relevance',
 'https://www.kroger.com/pl/hard-candy/23004?pzn=relevance',
 'https://www.kroger.com/pl/gum/23002?pzn=relevance',
 'https://www.kroger.com/pl/mints/23006',
 'https://www.kroger.com/pl/cold-cough-flu/22011?pzn=relevance',
 'https://www.kroger.com/pl/allergy-sinus/22012?pzn=relevance',
 'https://www.kroger.com/pl/pain-fever/22005?pzn=relevance',
 'https://www.kroger.com/pl/children-s-medicine/22014?pzn=relevance',
 'https://www.kroger.com/pl/energy-stimulants/22008?pzn=relevance',
 'https://www.kroger.com/pl/diet-adult-nutrition/22010?pzn=relevance',
 'https://www.kroger.com/pl/digestive-health-nausea/22001?pzn=relevance',
 'https://www.kroger.com/pl/immune-system-supports/2201100003?pzn=relevance',
 'https://www.kroger.com/pl/sleep-aids/22006?pzn=relevance',
 'https://www.kroger.com/pl/multi-vitamins/2201300005?pzn=relevance',
 'https://www.kroger.com/pl/letter-vitamins/2201300001?pzn=relevance',
 'https://www.kroger.com/pl/children-s-vitamins/2201300002?pzn=relevance',
 'https://www.kroger.com/pl/minerals/2201300004?pzn=relevance',
 'https://www.kroger.com/pl/herbal-supplements/2201300003?pzn=relevance',
 'https://www.kroger.com/pl/nutrition-diet-supplements/2201300008?pzn=relevance',
 'https://www.kroger.com/pl/vitaminssupplements/1800100003?pzn=relevance',
 'https://www.kroger.com/pl/prenatalpostnatal-vitamins/2201300010?pzn=relevance',
 'https://www.kroger.com/pl/joint-health/2201300007?pzn=relevance',
 'https://www.kroger.com/pl/fish-oil-oils-omegas/2201300006?pzn=relevance',
 'https://www.kroger.com/pl/hair-skin-nailssupplements/2201300011?pzn=relevance',
 'https://www.kroger.com/pl/coq-10/2201300012?pzn=relevance',
 'https://www.kroger.com/pl/first-aid/22004?pzn=relevance',
 'https://www.kroger.com/pl/foot-care/22007?pzn=relevance',
 'https://www.kroger.com/pl/eye-care/22002?pzn=relevance',
 'https://www.kroger.com/pl/home-healthcare-solutions/22009?pzn=relevance',
 'https://www.kroger.com/pl/sexual-health/22015?pzn=relevance',
 'https://www.kroger.com/pl/hair-care/21002?pzn=relevance',
 'https://www.kroger.com/pl/oral-care/21003?pzn=relevance',
 'https://www.kroger.com/pl/body-moisturizers/21006?pzn=relevance',
 'https://www.kroger.com/pl/bath-shower/21013?pzn=relevance',
 'https://www.kroger.com/pl/feminine-care/21009?pzn=relevance',
 'https://www.kroger.com/pl/hand-soap-sanitizer/21007?pzn=relevance',
 'https://www.kroger.com/pl/deodorants-antiperspirant/21001?pzn=relevance',
 'https://www.kroger.com/pl/incontinence/21008?pzn=relevance',
 'https://www.kroger.com/pl/shaving-grooming/21004?pzn=relevance',
 'https://www.kroger.com/pl/shampoo/2000400001?pzn=relevance',
 'https://www.kroger.com/pl/conditioner/2100200002?pzn=relevance',
 'https://www.kroger.com/pl/hair-color/2100200003?pzn=relevance',
 'https://www.kroger.com/pl/hair-styling-tools-appliances/2000400008?pzn=relevance',
 'https://www.kroger.com/pl/hair-brushes-accessories/2100200001?pzn=relevance',
 'https://www.kroger.com/pl/facialtreatments/2000200004?pzn=relevance',
 'https://www.kroger.com/pl/facialmoisturizers/2000200001?pzn=relevance',
 'https://www.kroger.com/pl/facial-masks/2000200005?pzn=relevance',
 'https://www.kroger.com/pl/face-wipesmakeup-remover/2000100005?pzn=relevance',
 'https://www.kroger.com/pl/bath-shower/20005',
 'https://www.kroger.com/pl/sun-tanning/20006?pzn=relevance',
 'https://www.kroger.com/pl/eyes/2000100002?pzn=relevance',
 'https://www.kroger.com/pl/face/2000100007?pzn=relevance',
 'https://www.kroger.com/pl/lips/2000100006?pzn=relevance',
 'https://www.kroger.com/pl/nails/2000100003?pzn=relevance',
 'https://www.kroger.com/pl/tools-brushes/2000100001?pzn=relevance',
 'https://www.kroger.com/pl/fragrance/20003',
 'https://www.kroger.com/pl/food-snacks-&-beverages/44009?pzn=relevance',
 'https://www.kroger.com/pl/baby-formula/44008?pzn=relevance',
 'https://www.kroger.com/pl/bottle-feeding-pacifiers-and-teethers/44002?pzn=relevance',
 'https://www.kroger.com/pl/nursing/44001?pzn=relevance',
 'https://www.kroger.com/pl/burp-cloths-bibs/44003?pzn=relevance',
 'https://www.kroger.com/pl/diapers/46002?pzn=relevance',
 'https://www.kroger.com/pl/diaper-essentials/46001?pzn=relevance',
 'https://www.kroger.com/pl/body-&-hair-care/46005?pzn=relevance',
 'https://www.kroger.com/pl/health-&-safety/45?pzn=relevance',
 'https://www.kroger.com/pl/car-seats-stroller-travel/42?pzn=relevance',
 'https://www.kroger.com/pl/nursery/43?pzn=relevance',
 'https://www.kroger.com/pl/kitchen-appliances/28007?pzn=relevance',
 'https://www.kroger.com/pl/kitchen-tools-gadgets/28001?pzn=relevance',
 'https://www.kroger.com/pl/coffee-tea/28012?pzn=relevance',
 'https://www.kroger.com/pl/thermal-water-bottles/28005?pzn=relevance',
 'https://www.kroger.com/pl/cutlery-knife-accessories/28013?pzn=relevance',
 'https://www.kroger.com/pl/cookware/28008?pzn=relevance',
 'https://www.kroger.com/pl/bakeware/28009?pzn=relevance',
 'https://www.kroger.com/pl/kitchen-table-linens/28006?pzn=relevance',
 'https://www.kroger.com/pl/kitchen-maintenance/28016?pzn=relevance',
 'https://www.kroger.com/pl/reusable-bags-totes/28015?pzn=relevance',
 'https://www.kroger.com/pl/kitchen-storage-organization/28002?pzn=relevance',
 'https://www.kroger.com/pl/glassware-drinkware/28004?pzn=relevance',
 'https://www.kroger.com/pl/tableware/28003?pzn=relevance',
 'https://www.kroger.com/pl/serveware/28010?pzn=relevance',
 'https://www.kroger.com/pl/bar-wine-accessories/28011?pzn=relevance',
 'https://www.kroger.com/pl/silverware-flatware/28014?pzn=relevance',
 'https://www.kroger.com/pl/furniture/31?pzn=relevance',
 'https://www.kroger.com/pl/throwpillows-blankets/32006?pzn=relevance',
 'https://www.kroger.com/pl/rugs/32009?pzn=relevance',
 'https://www.kroger.com/pl/decorativeaccents/32005?pzn=relevance',
 'https://www.kroger.com/pl/wall-art/32017?pzn=relevance',
 'https://www.kroger.com/pl/curtains/32015?pzn=relevance',
 'https://www.kroger.com/pl/curtain-rods-and-hardware/32014?pzn=relevance',
 'https://www.kroger.com/pl/kids-bedding/38005?pzn=relevance',
 'https://www.kroger.com/pl/mattresses-pads-toppers/38006?pzn=relevance',
 'https://www.kroger.com/pl/sheets-and-pillowcases/38008?pzn=relevance',
 'https://www.kroger.com/pl/quilts/38001?pzn=relevance',
 'https://www.kroger.com/pl/blankets/38002?pzn=relevance',
 'https://www.kroger.com/pl/comforter-sets/38003?pzn=relevance',
 'https://www.kroger.com/pl/duvet-covers/38004?pzn=relevance',
 'https://www.kroger.com/pl/pillows/38007?pzn=relevance',
 'https://www.kroger.com/pl/bedding-accessories/38009?pzn=relevance',
 'https://www.kroger.com/pl/bath-towels-and-rugs/37007?pzn=relevance',
 'https://www.kroger.com/pl/bathroom-accessories/37002?pzn=relevance',
 'https://www.kroger.com/pl/bathroom-hardware/37003?pzn=relevance',
 'https://www.kroger.com/pl/shower/37006?pzn=relevance',
 'https://www.kroger.com/pl/bathroom-furniture/37001?pzn=relevance',
 'https://www.kroger.com/pl/bathroom-storage/37005?pzn=relevance',
 'https://www.kroger.com/pl/batteries/26003?pzn=relevance',
 'https://www.kroger.com/pl/Light-Bulbs/26002?pzn=relevance',
 'https://www.kroger.com/pl/storagesolutions/39005?pzn=relevance',
 'https://www.kroger.com/pl/school-office/35?pzn=relevance',
 'https://www.kroger.com/pl/craft-hobby/34?pzn=relevance',
 'https://www.kroger.com/pl/hardware-home-improvement/33?pzn=relevance',
 'https://www.kroger.com/pl/automotive/15043?pzn=relevance',
 'https://www.kroger.com/pl/as-seen-on-tv/15172?pzn=relevance',
 'https://www.kroger.com/pl/tvs-home-theater/29001?pzn=relevance',
 'https://www.kroger.com/pl/video-computer-gaming/29007?pzn=relevance',
 'https://www.kroger.com/pl/audio-mp3-players/29003?pzn=relevance',
 'https://www.kroger.com/pl/computers-laptops-tablets/29004?pzn=relevance',
 'https://www.kroger.com/pl/computer-supplies-accessories/29005?pzn=relevance',
 'https://www.kroger.com/pl/printers-supplies/29006?pzn=relevance',
 'https://www.kroger.com/pl/connected-home/29010?pzn=relevance',
 'https://www.kroger.com/pl/fitness/29009?pzn=relevance',
 'https://www.kroger.com/pl/cameras-camcorders/29008?pzn=relevance',
 'https://www.kroger.com/pl/phones/29002?pzn=relevance',
 'https://www.kroger.com/pl/grills-outdoor-cooking/24001?pzn=relevance',
 'https://www.kroger.com/pl/lawn-garden/24002',
 'https://www.kroger.com/pl/patio-furniture/24003',
 'https://www.kroger.com/pl/action-figures-playsets/25002?pzn=relevance',
 'https://www.kroger.com/pl/dolls-preschool-baby/25004?pzn=relevance',
 'https://www.kroger.com/pl/games-puzzles/25001?pzn=relevance',
 'https://www.kroger.com/pl/outdoor-riding-remote-control/25003?pzn=relevance',
 'https://www.kroger.com/pl/creative-activity-educational/25005?pzn=relevance',
 'https://www.kroger.com/pl/costumes-dress-up/25006?pzn=relevance',
 'https://www.kroger.com/pl/trading-cards/2500100006?pzn=relevance']
    baseurl = 'https://www.kroger.com'

    headers = {
    'authority': 'www.kroger.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'bm_sz=E5FBDC2606E4FCB39A63BD11EE07E6DA~YAAQxqs0F3Bz3ZaJAQAASVMBmRRRj6GyURtX3as0mQo4wvZsMLecTPwVlDAnFYgzfdpLVrJrCs3n3Zyw2Y7moapFiZBTrqmHrhfMozRNQpCzv2H71DGaQL/IsizioODVmsJHMg1Ax3qgxAAh6SOhi8Q8GuKgYuT/lO3PITmANATJ1Oi4vXZqtDDGt8CcPneBotn/PNacriQ4AM/qCk2o0CKrU+vGOEp/AE/060caFtlWl2Vnx7QlDa0tV9SW+g14H2jULmBEa/bWzdJMckAgxGRTr0glH4Jh6xfTLHY+FOvXtDo1vL9VNw948Cnb+5SfXTQaHqLowDMuAYFywckZlP9PVn9E3Rwdes8uU3rOwR+fmiimGmZJvUy2RFHkOtR2x+C1EKnsaGUfw4pySus=~3160130~3160133; origin=fldc; dtCookie=v_4_srv_39_sn_A1BFE7456B3F1D741D1366DF30BB8368_perc_100000_ol_0_mul_1_app-3A81222ad3b2deb1ef_1_rcs-3Acss_0; sid=50f91b4f-5bfd-187c-038f-a8ad53eba395; pid=038fa8ad-53eb-50f9-a395-1b4f5bfd187c; AMCVS_371C27E253DB0F910A490D4E%40AdobeOrg=1; bm_mi=55AA3D5BEEA832371C51F0A86E1DE4C7~YAAQ22rcF0CWsJOJAQAAmZgGmRRvhDbiXkg4T6lK5ez/mlYdM9oyse/OR+KT+U6Io3vxDSplCNKIYJpXi/FgUMwrILFQd1T89BaxqBWoFNT5gMlAHyl2BXb+a6oMuzLUdLaFJxrUMcW5bMhuX4VjrtrmV0U93RZTLam1BcfR6/WmBcvkLF12AcivJBmokPV9B99sNfsljMSb+aweRbbZWkcfJsaAL6M6s+gmpv2y6THsKizF5crbiP9zhu+x5Nufuo6pKeNy1IO5H+vzMwcNtnzcV+ThGfKo4ZLz4P6OItHs6qaj45JLQ9Jfs4SUVkdYRdYtguG9CLIBNA4OTCfLwcA=~1; bm_sv=BBF7E81580B090C9750DE14E143CAFF0~YAAQ22rcF6mdsJOJAQAAx9MGmRQKmMlMaQfkT7RV/Z38QRn85twlQujJ0TGra3vg4an/Km+ngX7sk7LaTd2teSiPvJB1eSFg+bQKpmIsOCweYhR6Vny0tT6eHeIInBsHn3dewoL8JT2VrraVNnUc/ZDQDbAalfom1P08ixgUEbKzWfZhkYOZNVuBHkYesZlGLc9KUFgoAe8HhTnuscdOvHzuwKT+/akZak8QdRycJ2P/1OiBFLpxn/wUrJk5tvGSqw==~1; ak_bmsc=02A0ED49ED0BC3B440E3C51414B1A843~000000000000000000000000000000~YAAQ22rcF+qesJOJAQAAL+QGmRRbMUD9weaLKMcsSUdDK3VgeL3eUv9qiQQRMaK5DVr7z6axCNlfTMZp/rTtis3FQMqSGqUcGo/dDQjimLxcYbyhWu4YW878PVDJnhFwrGLVBanikmD2kt2qrYHKDAS6c+e0n/EL1E7W6PWnedEhAYMguC8expndPtjqfln20u0YOmSxJJIki1Lph4PLfzRVlL7jGD8DQDwDISRCxGl/ow+hkHFn4Y3j27mxVN6fZBwp918HxCTCCLQPrCQ4sBu356XJj6AvO/bpr6kalv9MotCyuzrp7IgY9JGhGiI+XbC0fJRVCP3SmLCRhZqsckzh+e2fZUFphUkUERL6EV7BravEDGmQxuk2953IJNdON0VPxWQGMGPFmp/I76dK3lulhJ4nt1WH6nwht3R4egNXnvxw6Sth6/g6o5ejLo2DlplOgg==; akaalb_KT_Digital_BannerSites=~op=KT_Digital_BannerSites_GCP_Search_East1:gcpsearcheast1|KT_CT_Banner_Prod_GCP_ALayer_Atlas_Recommendations_v1_East:bannersites-prod-gcp-recommendations-api-v1-prod-us-east1|KT_Digital_BannerSites_KCVG_HDC_FailoverCDC:hdc|~rv=74~m=gcpsearcheast1:0|bannersites-prod-gcp-recommendations-api-v1-prod-us-east1:0|hdc:0|~os=49d9e32c4b6129ccff2e66f9d0390271~id=aba402936a9b504be5071c6b617f238d; abTest=TL_94ad9f_C|TL_9b1a45_C|f7_2f03b8_C|2e_4d3fa9_B|8f_22d85b_B; s_cc=true; BVBRANDID=60258cd0-ab33-4d22-9f1e-f87f6d52e606; JSESSIONID=E4D1D90520E7DD47DBBE6272E1E0FE79; AMCV_371C27E253DB0F910A490D4E%40AdobeOrg=179643557%7CMCIDTS%7C19566%7CMCMID%7C40152213949085332185207238796172224260%7CMCAID%7CNONE%7CMCOPTOUT-1690499357s%7CNONE%7CvVersion%7C5.5.0%7CMCAAMLH-1691096957%7C9%7CMCAAMB-1691096957%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI; session_id=9d2603a1-1010-4072-96b3-65df1a62283c; _pin_unauth=dWlkPU5qVmlNVGM0TVdVdE9EWmpNUzAwWXpJMkxXSmtaREl0TVdNMFlXVmtZamd6T0RobA; _gcl_au=1.1.207043341.1690492369; AKA_A2=A; rxVisitor=1690493298989HV8KURNOIHVT8SLOA3VS1HGF2NGMBS11; productDetails=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; s_ips=707; dtSa=-; BVBRANDSID=c61e6bda-5d93-4d16-bc74-7cdd38d6c3a6; _abck=4444699C83C4AA88793A499964AA84A1~-1~YAAQZMMvFynyboeJAQAAMFJYmQqmVlRQmNuhsxNzZS5XZpI2Q18vA3P0zDc8IL6elhJwGs7cQdkQRPkAZxLbj68Zi5PDCp8l4SdUcKbEbq6SNFaIxnHQQ5F+sGpVgM2GtU0/cW2nIXS8NI6yzJbDSUkbRMBWHmme7OeYWnfOijaKAPJCMpxIkVeX6n2/al8qGCZ9NXCfBcN6y5FTq3NbnlHY0xuG9c//5980iw44CJoxW6YwJ9R7Q2Qs+pPBVUJx03LKk0Njkgox1Pth6cxTfH+1BymL/Lcx5vBP0NF1MuwE4cPcbbwjF3VNIHTb2gYjkzOVHmzjV97M94JglKwv+eIYB/uQMBmj5qBi8BLClH1PDx2Kn8jy/B2d6JaOdXrhmehw6PuboyIeAdAbEG+o14xxtP/KwDdK2D407+japEmJhYLDA38MG09PXKEmqpHLxFF9njh2RiLKpYLi81sDIKVVf2shkR8MSBQ10es6MRH6gHRvvuKy0fMj2Df5~-1~-1~1690498375; s_tslv=1690494863566; s_tp=2591; s_ppv=bn%253Aproducts%253Adetail%2C27%2C27%2C707%2C1%2C3; _uetsid=d99fce402cc111eebf397f2efd7022ee; _uetvid=d9a18db02cc111eebde23f0486d407a1; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+28+2023+02%3A54%3A28+GMT%2B0500+(Pakistan+Standard+Time)&version=202306.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=564071a2-52fe-4c1d-880e-404d3feec816&interactionCount=1&landingPath=NotLandingPage&groups=BG869%3A1%2CC0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0009%3A1%2CC0008%3A1&AwaitingReconsent=false&geolocation=US%3B; OptanonAlertBoxClosed=2023-07-27T21:54:28.524Z; x-active-modality={"postalCode":"20146","type":"SHIP","lat":39.01945496,"lng":-77.4618988,"source":"FALLBACK_ACTIVE_MODALITY_COOKIE","createdDate":1690494871409}; dtLatC=36; RT="z=1&dm=kroger.com&si=hke9m479xli&ss=lklllffe&sl=0&tt=0"; tslvc=1690494882110; rxvt=1690496684835|1690493298993; dtPC=39$294877260_714h1vPARLSCWCGQGUAQCPATUMTAIHCHQQLJHS-0e0; umid=5e587bd1-925c-48b3-afc7-b16a737efa3e',
    'device-memory': '8',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url,callback=self.pagination,)

    # def pagination(self,response):

    #     try:
    #         totalitems = int(response.xpath("//h2[@data-testid = 'SearchGridHeader-products']/text()").get().split(' ')[0].replace(',',''))
    #     except AttributeError:
    #         yield scrapy.Request(response.url,callback=self.pagination,)
    #         return
    #     itemsperpage= 24
    #     for pageno in range(1,math.ceil(totalitems/itemsperpage)+1):
    #         pageurl = response.url + f'&page={pageno}'
    #         yield scrapy.Request(pageurl,dont_filter =True,callback = self.getProducts,)
        
    # def getProducts(self,response):
        
    #     for url in [urljoin(self.baseurl,i) for i in response.xpath("//div[@class = 'AutoGrid-cell min-w-0']/div/div[@data-qa = 'cart-page-item-image']/a/@href").extract()]:
    #         yield scrapy.Request(url,dont_filter=True,callback = self.parse,meta={'retry':True})

    def start_requests(self):
        f = open("urls2.txt","r")
        urls = f.read()
        links = urls.split('\n')
        for link in links:
            yield scrapy.Request(link,callback = self.parse,meta={'retry':True})

    def parse(self, response):
        meta = response.meta
        retry = meta.get('retry')
        try:
            _,Category,SubCategory = response.xpath("//a[@class = 'kds-Link kds-Link--inherit mr-4']/text()").extract()
        except ValueError:
            if retry:
                yield scrapy.Request(response.url,dont_filter = True,callback=self.parse,meta={'retry':False})
                return
            else:
                f = open('urls3.txt','a')
                f.write(response.url+'\n')
                f.close()
                return
        ProductName = response.xpath("//h1[@class = 'ProductDetails-header font-bold']/text()").get(default = response.xpath("//h1[contains(@class,'ProductDetails')]/text()").get(default = 'N/A'))
        WholePrice = response.xpath("//span[@class = 'kds-Price-promotional-dropCaps']/text()").get(default = 0)
        DeciPrice = response.xpath("//sup[@class = 'kds-Price-superscript'][2]/text()").get(default = 0)
        Price = f"{WholePrice}.{DeciPrice}"

        items = {}
        items['StoreName'] = 'Kroger'
        items['ProductCategory'] = Category
        items['ProductSubcategory'] = SubCategory
        items['ProductURL'] = response.url
        items['ProductTitle'] = ProductName
        items['ProductBrand'] = ProductName
        items['ProductPrice'] = Price
        yield items
