# -*- coding: utf-8 -*-
"""FLYWAY content source. Add a dict here, run render.py, done."""
from svgs import SVG_RIVER, SVG_MTN, SVG_CITY

POSTS = [
 dict(id='01', type='statement', eyebrow='The name', size=168, foot='Est. 2027',
      head='Flyway.',
      sub='There is a migration corridor running from Southeast Asia to the Korean peninsula. '
          'Fifty million bodies move along it every season, chasing air. '
          'We built a running trip on the same line.',
      caption='ฟลายเวย์\n\nมีเส้นทางอพยพเส้นหนึ่ง ลากจากเอเชียตะวันออกเฉียงใต้ขึ้นไปถึงคาบสมุทรเกาหลี\nทุกฤดูกาล มีสิ่งมีชีวิตห้าสิบล้านชีวิตเคลื่อนตัวไปตามเส้นนั้น เพื่อตามหาอากาศ\n\nเราสร้างทริปวิ่งขึ้นมาบนเส้นเดียวกัน\n\n#Flyway #FlywayRunTrip #RunSeoul'),

 dict(id='02', type='statement', eyebrow='Run Trip 01 &middot; Seoul', size=140,
      head='Seoul is<br>the course.', foot='Bangkok &rarr; Seoul',
      sub='Not a tour. Not a race expo. Three roads Seoul crews actually run.',
      caption='โซลไม่ใช่ปลายทาง โซลคือเส้นทาง\n\nไม่ใช่ทัวร์ ไม่ใช่งานวิ่ง แต่คือสามเส้นทางที่ครูว์เกาหลีวิ่งกันจริง ๆ\nเมษายน 2027\n\n#Flyway #FlywayRunTrip #RunSeoul'),

 dict(id='03', type='stat', eyebrow='Why Korea &middot; 01', value='12&deg;C', size=290,
      label='Seoul &middot; 05:30 &middot; late April', foot='Why April',
      sub='The temperature distance runners actually train for. You cannot build it on a treadmill.',
      caption='ตีห้าครึ่งที่โซล ปลายเมษายน 12 องศา\n\nอุณหภูมิที่นักวิ่งระยะไกลใช้ซ้อมจริง ๆ และเป็นสิ่งเดียวที่ซ้อมเท่าไหร่ก็สร้างเองไม่ได้\n\n#Flyway #RunSeoul'),

 dict(id='04', type='statement', eyebrow='The three sessions', size=118,
      head='River.<br>Mountain.<br>City.', foot='Three mornings',
      sub='Three completely different runs. Nothing repeated, nothing looped twice.',
      caption='แม่น้ำ ภูเขา เมือง\n\nสามเส้นทาง สามแบบที่ไม่เหมือนกันเลย ไม่มีวิ่งวนซ้ำแม้แต่รอบเดียว\n\n#Flyway #FlywayRunTrip'),

 dict(id='05', type='route', eyebrow='Session 01 / River', head='Into<br>the sunset.',
      name='Banpo &rarr; Nodeulseom', svg=SVG_RIVER, foot='Friday 18:30',
      rows=[('Distance','6&ndash;7 km, out and back'),('Terrain','Flat riverside, no traffic lights'),
            ('You pass','Jamsu bridge, Sebitseom, Nodeulseom'),('Sunset','19:10')],
      caption='เซสชั่น 1 · ฮันกัง\nบันโพ ไป โนดึลซอม ไป-กลับ 6-7 กม.\n\nทางราบริมแม่น้ำ ไม่มีไฟแดงสักแยก วิ่งออกไปทางตะวันตกตอนพระอาทิตย์ตก แล้ววิ่งกลับใต้สะพานที่เปิดไฟ\n\n#Flyway #HanRiver'),

 dict(id='06', type='route', eyebrow='Session 02 / Mountain', head='The hill you<br>cannot train for.',
      name='Namsan summit', svg=SVG_MTN, foot='Saturday 08:00',
      rows=[('Distance','3&ndash;4 km, one course'),('Climb','about +200 m'),
            ('Terrain','Mountain road'),('At the top','N Seoul Tower')],
      caption='เซสชั่น 2 · นัมซาน\n3-4 กม. ขึ้นเขา ชันประมาณ 200 เมตร\n\nกรุงเทพไม่มีเนินแบบนี้ และวิ่งในสวนราบ ๆ ก็เตรียมตัวให้ไม่ได้ กติกามีข้อเดียว เจอกันข้างบน\n\n#Flyway #Namsan'),

 dict(id='07', type='route', eyebrow='Session 03 / City', head='Five landmarks.<br>Zero tourists.',
      name='Gwanghwamun loop', svg=SVG_CITY, foot='Sunday 07:30',
      rows=[('Distance','7.8 km full, 4 km short'),('Terrain','City streets, gentle'),
            ('You pass','Cheonggyecheon, Bukchon, Gyeongbokgung'),('Finish','Gwanghwamun Square')],
      caption='เซสชั่น 3 · ควังฮวามุน\n7.8 กม. เต็มลูป หรือ 4 กม. ครึ่งทาง\n\nทุกจุดบนเส้นทางนี้คนแน่นตั้งแต่สิบโมง แต่เจ็ดโมงครึ่งวันอาทิตย์ มันว่างและมันเป็นของเรา\n\n#Flyway #Gwanghwamun'),

 dict(id='08', type='compare', eyebrow='Bangkok vs Seoul &middot; 05:30', foot='Why April',
      a=dict(label='Bangkok &middot; 05:30', value='28&deg;C', note='85% humidity'),
      b=dict(label='Seoul &middot; 05:30 &middot; late April', value='12&deg;C', note='dry air'),
      sub='Sixteen degrees. That gap is the whole reason this trip exists.',
      caption='ตีห้าครึ่ง ที่กรุงเทพ 28 องศา ความชื้น 85%\nตีห้าครึ่ง ที่โซลปลายเมษายน 12 องศา อากาศแห้ง\n\nต่าง 16 องศา และนั่นคือเหตุผลทั้งหมดของทริปนี้\n\n#Flyway #RunSeoul'),

 dict(id='09', type='compare', eyebrow='The climb', foot='Session 02',
      a=dict(label='Lumphini loop', value='+0m', note='flat, every lap the same'),
      b=dict(label='Namsan summit', value='+200m', note='road to the tower'),
      sub='A flat park will never prepare anyone for a real climb. That is the point of session two.',
      caption='สวนลุมฯ ชัน 0 เมตร วนกี่รอบก็เหมือนเดิม\nนัมซาน ชัน 200 เมตร ถนนขึ้นไปถึงหอคอย\n\nวิ่งสวนราบ ๆ เตรียมตัวสำหรับเนินจริงไม่ได้ นั่นแหละคือประเด็นของเซสชั่นสอง\n\n#Flyway #Namsan'),

 dict(id='10', type='statement', eyebrow='Why April', size=104, theme='lite', foot='Late April',
      head='You cannot<br>train for<br>weather.',
      sub='You can only travel to it. March is still cold, May turns warm, and late April is the week Seoul was built for running.',
      caption='อากาศเป็นสิ่งเดียวที่ซ้อมเองไม่ได้ ทำได้อย่างเดียวคือบินไปหามัน\n\nมีนาคมยังหนาว พฤษภาคมเริ่มร้อน ปลายเมษายนคือสัปดาห์ที่โซลถูกสร้างมาเพื่อการวิ่ง\n\n#Flyway'),

 dict(id='11', type='stat', eyebrow='Recon &middot; Han river', value='05:34', size=250,
      label='Sunrise &middot; Seoul &middot; late April', foot='Recon',
      sub='First light on the river. We are walking every route before anyone runs it.',
      caption='พระอาทิตย์ขึ้น 05:34 ที่โซล ปลายเมษายน\n\nเราเดินสำรวจทุกเส้นทางเองก่อน ก่อนที่จะมีใครได้วิ่งมันจริง ๆ\n\n#Flyway #RunSeoul'),

 dict(id='12', type='statement', eyebrow='Run Trip 01 &middot; Spring 2027', size=126,
      theme='volt', head='April.<br>Seoul.<br>You.', foot='Bangkok &rarr; Seoul',
      sub='Dates tentative. Routes confirmed. More soon.',
      caption='เมษายน โซล และคุณ\n\nวันที่ยังไม่ฟิกซ์ เส้นทางฟิกซ์แล้ว เดี๋ยวมีมาอีก\n\n#Flyway #FlywayRunTrip #RunSeoul'),
]
