from PIL import Image
from django.core.management import BaseCommand

from face_detection.services import detector

images = ["/Users/sebastiaan/Desktop/100CANON/IMG_5016.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5017.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5018.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5019.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5020.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5021.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5022.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5023.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5024.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5025.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5026.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5027.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5028.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5029.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5030.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5031.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5032.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5033.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5034.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5035.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5036.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5037.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5038.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5039.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5040.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5041.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5042.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5043.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5044.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5045.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5046.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5047.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5048.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5049.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5050.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5051.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5052.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5053.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5054.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5055.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5056.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5057.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5058.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5059.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5060.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5061.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5062.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5063.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5064.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5065.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5066.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5067.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5068.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5069.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5070.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5071.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5072.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5073.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5074.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5075.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5076.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5077.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5078.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5079.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5080.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5081.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5082.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5083.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5084.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5085.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5086.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5087.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5088.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5089.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5090.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5091.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5092.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5093.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5094.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5095.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5096.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5097.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5098.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5099.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5100.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5101.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5102.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5103.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5104.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5105.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5106.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5107.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5108.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5109.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5110.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5111.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5112.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5113.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5114.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5115.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5116.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5117.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5118.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5119.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5120.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5121.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5122.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5123.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5124.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5125.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5126.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5127.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5128.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5129.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5130.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5131.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5132.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5133.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5134.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5135.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5136.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5137.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5138.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5139.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5140.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5141.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5142.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5143.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5144.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5145.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5146.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5147.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5148.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5149.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5150.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5151.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5152.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5153.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5154.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5155.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5156.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5157.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5158.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5159.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5160.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5161.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5162.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5163.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5164.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5165.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5166.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5167.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5168.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5169.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5170.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5171.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5172.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5173.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5174.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5175.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5176.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5177.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5178.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5179.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5180.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5181.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5182.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5183.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5184.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5185.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5186.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5187.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5188.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5189.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5190.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5191.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5192.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5193.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5194.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5195.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5196.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5197.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5198.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5199.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5200.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5201.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5202.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5203.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5204.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5205.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5206.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5207.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5208.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5209.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5210.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5211.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5212.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5213.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5214.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5215.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5216.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5217.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5218.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5219.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5220.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5221.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5222.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5223.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5224.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5225.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5226.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5227.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5228.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5229.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5230.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5231.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5232.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5233.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5234.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5235.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5236.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5237.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5238.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5239.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5240.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5241.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5242.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5243.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5244.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5245.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5246.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5247.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5248.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5249.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5250.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5251.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5252.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5253.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5254.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5255.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5256.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5257.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5258.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5259.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5260.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5261.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5262.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5263.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5264.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5265.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5266.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5267.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5268.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5269.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5270.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5271.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5272.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5273.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5274.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5275.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5276.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5277.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5278.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5279.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5280.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5281.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5282.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5283.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5284.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5285.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5286.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5287.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5288.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5289.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5290.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5291.JPG",
          "/Users/sebastiaan/Desktop/100CANON/IMG_5292.JPG"]


class Command(BaseCommand):
    help = 'Import the face encodings of an image into the database'

    def add_arguments(self, parser):
        parser.add_argument('image_location', type=str)

    def handle(self, *args, **options):
        encodings = detector.obtain_encodings(1, options['image_location'])
        pks = [encoding.pk for encoding in encodings]
        results = detector.search_persons(pks)
        for encoding in encodings:
            encoding.delete()

        for result in results:
            self.stdout.write(images[result])
            Image.open(images[result]).show()
