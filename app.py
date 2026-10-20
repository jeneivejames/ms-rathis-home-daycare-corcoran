import os
from flask import Flask, render_template_string, send_from_directory

def _find_static():
    """Locate the static/ folder reliably (local, Databricks, and Vercel lambda)."""
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (
        os.path.join(here, 'static'),                    # normal layout
        os.path.join(os.path.dirname(here), 'static'),   # lambda may nest api/index.py
        os.path.join(os.getcwd(), 'static'),             # lambda cwd
        os.path.join(os.getcwd(), '..', 'static'),       # lambda cwd parent
    ):
        if os.path.isdir(cand):
            return cand
    return os.path.join(here, 'static')

app = Flask(__name__, static_folder=_find_static())

# Case-insensitive image serving: works whether files are .jpg or .JPG
# (GitHub upload created .JPG; Vercel's Linux filesystem is case-sensitive)
@app.route('/static/images/<path:filename>')
def case_insensitive_images(filename):
    img_dir = os.path.join(app.static_folder, 'images')
    target = os.path.join(img_dir, filename)
    if not os.path.exists(target):
        base, ext = os.path.splitext(filename)
        for e in ('.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG'):
            alt = base + e
            if os.path.exists(os.path.join(img_dir, alt)):
                return send_from_directory(img_dir, alt)
    return send_from_directory(img_dir, filename)

HTML_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ms. Rathi\'s Home Daycare | Learn. Love. Grow.</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  html{overflow-x:hidden;scroll-behavior:smooth;}
  body{overflow-x:hidden;font-family:'Nunito',sans-serif;color:#2d3748;background:#fff;}
  ::-webkit-scrollbar{width:8px;}
  ::-webkit-scrollbar-track{background:#f7fafc;}
  ::-webkit-scrollbar-thumb{background:#cbd5e0;border-radius:4px;}

  /* NAV */
  nav{position:fixed;top:0;width:100%;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);box-shadow:0 1px 20px rgba(0,0,0,.06);z-index:100;display:flex;align-items:center;padding:0 6vw;height:72px;transition:.3s;}
  nav.scrolled{box-shadow:0 2px 30px rgba(0,0,0,.08);}
  .nav-logo{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:900;color:#2d3748;}
  .nav-logo span{color:#f08850;}
  .nav-links{margin-left:auto;display:flex;gap:36px;align-items:center;}
  .nav-links a{text-decoration:none;color:#4a5568;font-weight:700;font-size:.98rem;transition:.2s;position:relative;}
  .nav-links a:hover{color:#f08850;}
  .nav-links a:after{content:'';position:absolute;bottom:-4px;left:0;width:0;height:2px;background:#f08850;transition:.3s;}
  .nav-links a:hover:after{width:100%;}
  .nav-cta{background:linear-gradient(135deg,#f08850,#f6ad55);color:#fff!important;padding:12px 32px;border-radius:50px;font-weight:800;box-shadow:0 4px 15px rgba(240,136,80,.3);transition:.2s;}
  .nav-cta:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(240,136,80,.4);}
  .nav-cta:after{display:none;}
  .hamburger{display:none;font-size:1.8rem;cursor:pointer;background:none;border:none;color:#2d3748;}

  /* HERO */
  .hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden;}
  .hero-bg{position:absolute;inset:0;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);z-index:0;}
  .hero-bg:before{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(102,126,234,.3) 0%,rgba(118,75,162,.5) 100%);z-index:1;}
  .hero-slider{position:absolute;inset:0;z-index:0;}
  .hero-slide{position:absolute;inset:0;opacity:0;transition:opacity 1.5s ease-in-out;background:linear-gradient(135deg,#fde8d7 0%,#fef9f5 45%,#fbd38d 100%);}
  .hero-slide.active{opacity:1;}
  .hero-slide-bg{position:absolute;inset:-40px;background-size:cover;background-position:center;filter:blur(8px);opacity:.8;transform:scale(1.08);}
  .hero-slide img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;}
  .hero-overlay{position:absolute;inset:0;background:linear-gradient(180deg,rgba(45,55,72,.02) 0%,rgba(45,55,72,.22) 100%);z-index:2;}
  .hero-content{position:relative;z-index:3;max-width:800px;padding:0 20px;}
  .hero-content h1{font-family:'Playfair Display',serif;font-size:4.2rem;color:#fff;line-height:1.1;margin-bottom:20px;text-shadow:0 4px 30px rgba(0,0,0,.3);}
  .hero-content h1 span{color:#fbd38d;}
  .hero-content p{font-size:1.3rem;color:rgba(255,255,255,.92);margin-bottom:40px;font-weight:400;line-height:1.6;}
  .hero-btns{display:flex;gap:18px;justify-content:center;flex-wrap:wrap;}
  .btn-primary{background:linear-gradient(135deg,#f08850,#f6ad55);color:#fff;padding:16px 44px;border-radius:50px;text-decoration:none;font-weight:800;font-size:1.05rem;box-shadow:0 6px 25px rgba(240,136,80,.4);transition:.25s;}
  .btn-primary:hover{transform:translateY(-3px);box-shadow:0 10px 35px rgba(240,136,80,.5);}
  .btn-outline{background:rgba(255,255,255,.12);backdrop-filter:blur(8px);color:#fff;border:2px solid rgba(255,255,255,.5);padding:16px 44px;border-radius:50px;text-decoration:none;font-weight:700;font-size:1.05rem;transition:.25s;}
  .btn-outline:hover{background:rgba(255,255,255,.2);border-color:#fff;}
  .scroll-indicator{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);z-index:3;color:#fff;font-size:1.5rem;animation:bounce 2s infinite;cursor:pointer;text-decoration:none;}
  @keyframes bounce{0%,100%{transform:translateX(-50%) translateY(0);}50%{transform:translateX(-50%) translateY(12px);}}

  /* SECTIONS */
  .section{padding:90px 6vw;position:relative;}
  .section-center{max-width:1200px;margin:0 auto;}
  .section-tag{text-align:center;font-size:.85rem;font-weight:800;letter-spacing:3px;text-transform:uppercase;color:#f08850;margin-bottom:12px;}
  .section-title{text-align:center;font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#2d3748;margin-bottom:16px;}
  .section-sub{text-align:center;font-size:1.15rem;color:#718096;max-width:600px;margin:0 auto 50px;line-height:1.6;}

  /* ABOUT */
  .about{background:#fef9f5;}
  .about-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;}
  .about-img{border-radius:24px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.12);position:relative;}
  .about-img img{width:100%;height:420px;object-fit:cover;transition:.5s;}
  .about-img:hover img{transform:scale(1.05);}
  .about-text h2{font-family:'Playfair Display',serif;font-size:2.4rem;color:#2d3748;margin-bottom:20px;line-height:1.2;}
  .about-text p{font-size:1.1rem;color:#718096;line-height:1.8;margin-bottom:16px;}
  .about-features{display:flex;flex-wrap:wrap;gap:14px;margin-top:24px;}
  .about-feature{display:flex;align-items:center;gap:10px;background:#fff;padding:12px 20px;border-radius:50px;box-shadow:0 4px 15px rgba(0,0,0,.05);font-weight:700;font-size:.95rem;color:#4a5568;}
  .about-feature span{font-size:1.3rem;}

  /* PROGRAMS */
  .programs{background:#fff;}
  .programs-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:30px;}
  .program-card{background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 10px 40px rgba(0,0,0,.07);transition:.3s;border:1px solid #edf2f7;position:relative;}
  .program-card:hover{transform:translateY(-8px);box-shadow:0 20px 50px rgba(0,0,0,.12);}
  .program-card-img{height:200px;overflow:hidden;position:relative;}
  .program-card-img img{width:100%;height:100%;object-fit:cover;transition:.5s;}
  .program-card:hover .program-card-img img{transform:scale(1.1);}
  .program-age{position:absolute;top:15px;right:15px;background:linear-gradient(135deg,#f08850,#f6ad55);color:#fff;padding:6px 18px;border-radius:50px;font-size:.85rem;font-weight:800;box-shadow:0 4px 12px rgba(240,136,80,.3);}
  .program-card-body{padding:28px 24px;}
  .program-card-body h3{font-family:'Playfair Display',serif;font-size:1.5rem;color:#2d3748;margin-bottom:12px;}
  .program-card-body p{color:#718096;font-size:.98rem;line-height:1.6;margin-bottom:16px;}
  .program-card-body ul{list-style:none;padding:0;}
  .program-card-body ul li{padding:5px 0 5px 26px;position:relative;color:#4a5568;font-size:.93rem;}
  .program-card-body ul li:before{content:'\u2714';position:absolute;left:0;color:#f08850;font-weight:bold;}
  .program-icon{position:absolute;top:20px;left:20px;background:rgba(255,255,255,.9);width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;box-shadow:0 4px 15px rgba(0,0,0,.1);}

  /* WHY US */
  .whyus{background:linear-gradient(135deg,#2d3748 0%,#1a202c 100%);color:#fff;}
  .whyus .section-title{color:#fff;}
  .whyus .section-sub{color:rgba(255,255,255,.7);}
  .whyus .section-tag{color:#fbd38d;}
  .whyus-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:24px;}
  .whyus-card{text-align:center;padding:40px 20px;background:rgba(255,255,255,.06);border-radius:20px;border:1px solid rgba(255,255,255,.08);transition:.3s;}
  .whyus-card:hover{background:rgba(255,255,255,.1);transform:translateY(-5px);}
  .whyus-card .icon{font-size:2.5rem;margin-bottom:16px;display:block;}
  .whyus-card h4{font-size:1.05rem;font-weight:800;margin-bottom:8px;}
  .whyus-card p{font-size:.88rem;color:rgba(255,255,255,.6);line-height:1.5;}

  /* GALLERY */
  .gallery{background:#fef9f5;}
  .gallery-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;}
  .gallery-item{border-radius:18px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,.08);cursor:pointer;position:relative;height:280px;}
  .gallery-item img{width:100%;height:100%;object-fit:cover;transition:.5s;}
  .gallery-item:hover img{transform:scale(1.12);}
  .gallery-item:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(45,55,72,.4) 100%);opacity:0;transition:.3s;}
  .gallery-item:hover:after{opacity:1;}

  /* TESTIMONIALS */
  .testimonials{background:#fff;}
  .test-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:30px;}
  .testimonial-card{background:#fef9f5;border-radius:20px;padding:36px 30px;box-shadow:0 8px 30px rgba(0,0,0,.05);position:relative;border:1px solid #fde8d7;}
  .testimonial-card .quote-icon{font-size:3rem;color:#fbd38d;font-family:'Playfair Display',serif;line-height:1;position:absolute;top:20px;right:30px;opacity:.4;}
  .testimonial-card .stars{color:#f6ad55;font-size:1.1rem;margin-bottom:14px;letter-spacing:3px;}
  .testimonial-card .text{font-size:1.05rem;color:#4a5568;line-height:1.7;font-style:italic;margin-bottom:20px;}
  .testimonial-card .author{display:flex;align-items:center;gap:14px;}
  .testimonial-card .author-avatar{width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#f08850,#f6ad55);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:1.2rem;}
  .testimonial-card .author-info .name{font-weight:800;color:#2d3748;font-size:1rem;}
  .testimonial-card .author-info .role{font-size:.85rem;color:#a0aec0;}

  /* CONTACT */
  .contact{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:#fff;padding:90px 6vw;}
  .contact .section-title{color:#fff;}
  .contact .section-tag{color:#fbd38d;}
  .contact .section-sub{color:rgba(255,255,255,.8);}
  .contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:50px;max-width:1100px;margin:0 auto;}
  .contact-info h3{font-family:'Playfair Display',serif;font-size:1.8rem;margin-bottom:24px;}
  .contact-item{display:flex;align-items:center;gap:16px;margin-bottom:20px;}
  .contact-item .icon{width:50px;height:50px;border-radius:14px;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0;}
  .contact-item .label{font-size:.8rem;color:rgba(255,255,255,.6);text-transform:uppercase;letter-spacing:1px;}
  .contact-item .value{font-size:1.05rem;font-weight:700;}
  .contact-form{background:rgba(255,255,255,.1);backdrop-filter:blur(10px);border-radius:24px;padding:36px;border:1px solid rgba(255,255,255,.15);}
  .contact-form input,.contact-form textarea{width:100%;padding:14px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);color:#fff;font-size:.98rem;margin-bottom:14px;font-family:inherit;}
  .contact-form input::placeholder,.contact-form textarea::placeholder{color:rgba(255,255,255,.5);}
  .contact-form input:focus,.contact-form textarea:focus{outline:none;border-color:#fbd38d;background:rgba(255,255,255,.12);}
  .contact-form button{width:100%;background:linear-gradient(135deg,#f08850,#f6ad55);color:#fff;border:none;border-radius:12px;padding:16px;font-size:1.05rem;font-weight:800;cursor:pointer;transition:.2s;}
  .contact-form button:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(240,136,80,.4);}

  /* FOOTER */
  footer{background:#1a202c;color:rgba(255,255,255,.6);padding:50px 6vw 30px;text-align:center;}
  footer .footer-logo{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:900;color:#fff;margin-bottom:12px;}
  footer .footer-logo span{color:#f08850;}
  footer p{font-size:.95rem;margin-bottom:8px;}
  footer .social{margin:20px 0;display:flex;gap:16px;justify-content:center;}
  footer .social a{width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;font-size:1.2rem;color:#fff;text-decoration:none;transition:.2s;}
  footer .social a:hover{background:#f08850;transform:translateY(-3px);}
  footer .copyright{border-top:1px solid rgba(255,255,255,.08);padding-top:20px;margin-top:20px;font-size:.85rem;}

  /* ANIMATIONS */
  .fade-in{opacity:0;transform:translateY(40px);transition:opacity .8s ease,transform .8s ease;}
  .fade-in.visible{opacity:1;transform:translateY(0);}

  /* MOBILE */
  @media(max-width:900px){
    .hero-content h1{font-size:2.6rem;}
    .hero-content p{font-size:1.1rem;}
    .about-grid,.contact-grid{grid-template-columns:1fr;gap:30px;}
    .section-title{font-size:2rem;}
    .hero-slider img{object-fit:cover;}
    .hero-slide-bg{display:none;}
    .nav-links{display:none;position:fixed;top:72px;left:0;width:100%;background:#fff;flex-direction:column;padding:24px 6vw 30px;gap:18px;box-shadow:0 10px 30px rgba(0,0,0,.1);margin-left:0;align-items:flex-start;}
    .nav-links a{font-size:1.05rem;padding:2px 0;}
    .nav-links a:after{display:none;}
    .nav-links .nav-cta{display:block;width:100%;text-align:center;padding:14px 24px;margin-top:6px;}
    .nav-links.open{display:flex;}
    .hamburger{display:block;}
  }
  @media(max-width:500px){
    .hero-content h1{font-size:2rem;}
    .hero-btns{flex-direction:column;align-items:center;}
    .section{padding:60px 5vw;}
  }
</style>
</head>
<body>
  <nav id="navbar">
    <div class="nav-logo">Ms. Rathi\'s <span>Daycare</span></div>
    <div class="nav-links" id="navLinks">
      <a href="#about">About</a>
      <a href="#programs">Programs</a>
      <a href="#gallery">Gallery</a>
      <a href="#testimonials">Reviews</a>
      <a href="#contact" class="nav-cta">Schedule a Visit</a>
    </div>
    <button class="hamburger" id="hamburger" onclick="document.getElementById('navLinks').classList.toggle('open')">&#9776;</button>
  </nav>

  <div class="hero">
    <div class="hero-slider" id="heroSlider">
      <div class="hero-slide active">
        <div class="hero-slide-bg" style="background-image:url('/static/images/gallery3.jpg')"></div>
        <img src="/static/images/gallery1.jpg" alt="Daycare Photo 1">
      </div>
      <div class="hero-slide">
        <div class="hero-slide-bg" style="background-image:url('/static/images/gallery1.jpg')"></div>
        <img src="/static/images/gallery2.jpg" alt="Daycare Photo 2">
      </div>
      <div class="hero-slide">
        <div class="hero-slide-bg" style="background-image:url('/static/images/gallery5.jpg')"></div>
        <img src="/static/images/gallery3.jpg" alt="Daycare Photo 3">
      </div>
      <div class="hero-slide">
        <div class="hero-slide-bg" style="background-image:url('/static/images/gallery2.jpg')"></div>
        <img src="/static/images/gallery4.jpg" alt="Daycare Photo 4">
      </div>
      <div class="hero-slide">
        <div class="hero-slide-bg" style="background-image:url('/static/images/gallery4.jpg')"></div>
        <img src="/static/images/gallery5.jpg" alt="Daycare Photo 5">
      </div>
    </div>
    <div class="hero-overlay"></div>
    <div class="hero-content fade-in visible">
      <h1>Learn. Love. <span>Grow.</span></h1>
      <p>A nurturing, modern home-based daycare in Corcoran where every child is celebrated, inspired, and loved like family.</p>
      <div class="hero-btns">
        <a href="#programs" class="btn-primary">Explore Programs</a>
        <a href="#contact" class="btn-outline">Book a Tour</a>
      </div>
    </div>
    <a href="#about" class="scroll-indicator">&darr;</a>
  </div>

  <div class="section about" id="about">
    <div class="section-center">
      <div class="about-grid">
        <div class="about-img fade-in">
          <img src="/static/images/gallery5.jpg" alt="Daycare">
        </div>
        <div class="about-text fade-in">
          <div class="section-tag" style="text-align:left">About Us</div>
          <h2>Where Every Child Shines Bright</h2>
          <p>At Ms. Rathi\'s Home Daycare, we provide a warm, loving environment where children learn through play, exploration, and meaningful connections. Our small group sizes ensure personalized attention for every child.</p>
          <p>With years of experience and a passion for early childhood development, we create a space where your little one can thrive socially, emotionally, and academically.</p>
          <div class="about-features">
            <div class="about-feature"><span>&#10004;</span> Licensed & Certified</div>
            <div class="about-feature"><span>&#10004;</span> CPR/First Aid</div>
            <div class="about-feature"><span>&#10004;</span> Nutritious Meals</div>
            <div class="about-feature"><span>&#10004;</span> Daily Updates</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="section programs" id="programs">
    <div class="section-center">
      <div class="section-tag fade-in">Our Curriculum</div>
      <div class="section-title fade-in">Programs for Every Age</div>
      <div class="section-sub fade-in">Age-appropriate learning experiences designed to nurture growth at every stage of development.</div>
      <div class="programs-grid">
        <div class="program-card fade-in">
          <div class="program-card-img"><img src="https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=600&q=80" alt="Infant"></div>
          <div class="program-age">6w-18m</div>
          <div class="program-icon">&#128104;&#8205;&#128105;&#8205;&#128103;</div>
          <div class="program-card-body">
            <h3>Infant Care</h3>
            <p>Gentle, responsive care in a cozy, stimulating environment.</p>
            <ul><li>Individual feeding & nap schedules</li><li>Sensory & motor skill play</li><li>Loving bonding time</li></ul>
          </div>
        </div>
        <div class="program-card fade-in">
          <div class="program-card-img"><img src="/static/images/gallery1.jpg" alt="Toddler"></div>
          <div class="program-age">18m-3y</div>
          <div class="program-icon">&#129490;</div>
          <div class="program-card-body">
            <h3>Toddlers</h3>
            <p>Active exploration through play, music, and creative arts.</p>
            <ul><li>Language & social skills</li><li>Arts, crafts & music</li><li>Outdoor adventures</li></ul>
          </div>
        </div>
        <div class="program-card fade-in">
          <div class="program-card-img"><img src="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=600&q=80" alt="Preschool"></div>
          <div class="program-age">3y-4y</div>
          <div class="program-icon">&#127912;</div>
          <div class="program-card-body">
            <h3>Preschool</h3>
            <p>Building foundations in literacy, numeracy, and social skills.</p>
            <ul><li>Reading & math readiness</li><li>Science discovery</li><li>Friendship & teamwork</li></ul>
          </div>
        </div>
        <div class="program-card fade-in">
          <div class="program-card-img"><img src="/static/images/gallery4.jpg" alt="Pre-K"></div>
          <div class="program-age">4y-5y</div>
          <div class="program-icon">&#128218;</div>
          <div class="program-card-body">
            <h3>Pre-K</h3>
            <p>Kindergarten readiness with STEAM projects and independence.</p>
            <ul><li>Reading & writing skills</li><li>STEAM & nature projects</li><li>Confidence & independence</li></ul>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="section whyus">
    <div class="section-center">
      <div class="section-tag fade-in">Why Choose Us</div>
      <div class="section-title fade-in">The Ms. Rathi\'s Difference</div>
      <div class="section-sub fade-in">Six reasons families trust us with their most precious little ones.</div>
      <div class="whyus-grid">
        <div class="whyus-card fade-in"><span class="icon">&#127968;</span><h4>Small Groups</h4><p>Personalized care with low child-to-provider ratios.</p></div>
        <div class="whyus-card fade-in"><span class="icon">&#128105;&#8205;&#127979;</span><h4>Experienced</h4><p>Years of dedicated early childhood education.</p></div>
        <div class="whyus-card fade-in"><span class="icon">&#127858;</span><h4>Home-Cooked</h4><p>Nutritious, fresh meals prepared daily.</p></div>
        <div class="whyus-card fade-in"><span class="icon">&#129489;&#8205;&#128187;</span><h4>Daily Reports</h4><p>Real-time updates on your child\'s day.</p></div>
        <div class="whyus-card fade-in"><span class="icon">&#127795;</span><h4>Safe Space</h4><p>Clean, secure, and child-proofed environment.</p></div>
        <div class="whyus-card fade-in"><span class="icon">&#10084;</span><h4>Loving Care</h4><p>Every child treated as part of our family.</p></div>
      </div>
    </div>
  </div>

  <div class="section gallery" id="gallery">
    <div class="section-center">
      <div class="section-tag fade-in">Photo Gallery</div>
      <div class="section-title fade-in">A Glimpse Into Our Day</div>
      <div class="section-sub fade-in">See the joy, learning, and friendships that happen every day.</div>
      <div class="gallery-grid">
        <div class="gallery-item fade-in"><img src="/static/images/gallery1.jpg" alt="Gallery 1"></div>
        <div class="gallery-item fade-in"><img src="/static/images/gallery2.jpg" alt="Gallery 2"></div>
        <div class="gallery-item fade-in"><img src="/static/images/gallery3.jpg" alt="Gallery 3"></div>
        <div class="gallery-item fade-in"><img src="/static/images/gallery4.jpg" alt="Gallery 4"></div>
      </div>
    </div>
  </div>

  <div class="section testimonials" id="testimonials">
    <div class="section-center">
      <div class="section-tag fade-in">Testimonials</div>
      <div class="section-title fade-in">What Families Say</div>
      <div class="section-sub fade-in">Don\'t just take our word for it. Hear from the families who trust us.</div>
      <div class="test-grid">
        <div class="testimonial-card fade-in">
          <div class="quote-icon">&ldquo;</div>
          <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <div class="text">Ms. Rathi has been a blessing for our family. Our daughter has grown so much! The small group size means she truly knows each child\'s needs.</div>
          <div class="author"><div class="author-avatar">S</div><div class="author-info"><div class="name">Sarah M.</div><div class="role">Parent of a 3-year-old</div></div></div>
        </div>
        <div class="testimonial-card fade-in">
          <div class="quote-icon">&ldquo;</div>
          <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <div class="text">The curriculum is fantastic! My son went from barely talking to telling us stories about his day. The daily reports keep us connected to everything.</div>
          <div class="author"><div class="author-avatar">D</div><div class="author-info"><div class="name">David & Priya K.</div><div class="role">Parents of a 4-year-old</div></div></div>
        </div>
        <div class="testimonial-card fade-in">
          <div class="quote-icon">&ldquo;</div>
          <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
          <div class="text">I felt at peace the moment I walked in. The home is warm, clean, and filled with learning materials. My toddler runs to the door every morning!</div>
          <div class="author"><div class="author-avatar">J</div><div class="author-info"><div class="name">Jessica T.</div><div class="role">Parent of a 2-year-old</div></div></div>
        </div>
      </div>
    </div>
  </div>

  <div class="section contact" id="contact">
    <div class="section-center">
      <div class="section-tag fade-in">Get In Touch</div>
      <div class="section-title fade-in">Schedule a Visit Today</div>
      <div class="section-sub fade-in">We\'d love to welcome you and your little one. Reach out to schedule a tour.</div>
      <div class="contact-grid">
        <div class="contact-info fade-in">
          <h3>Visit Our Daycare</h3>
          <div class="contact-item"><div class="icon">&#128205;</div><div><div class="label">Location</div><div class="value">Corcoran, MN</div></div></div>
          <div class="contact-item"><div class="icon">&#128222;</div><div><div class="label">Phone</div><div class="value">(763) 555-0123</div></div></div>
          <div class="contact-item"><div class="icon">&#9993;</div><div><div class="label">Email</div><div class="value">msrathidaycare@example.com</div></div></div>
          <div class="contact-item"><div class="icon">&#128336;</div><div><div class="label">Hours</div><div class="value">Mon-Fri, 7:00 AM - 5:30 PM</div></div></div>
        </div>
        <form class="contact-form fade-in" onsubmit="alert('Thank you! We will contact you soon.'); return false;">
          <input type="text" placeholder="Your Name" required>
          <input type="email" placeholder="Email Address" required>
          <input type="text" placeholder="Phone Number">
          <textarea rows="3" placeholder="Message / Questions"></textarea>
          <button type="submit">Request a Tour</button>
        </form>
      </div>
    </div>
  </div>

  <footer>
    <div class="footer-logo">Ms. Rathi\'s <span>Daycare</span></div>
    <p>Nurturing children with love, learning, and joy in Corcoran, MN.</p>
    <div class="social">
      <a href="#">&#128247;</a><a href="#">&#128241;</a><a href="#">&#9993;</a>
    </div>
    <div class="copyright">&copy; 2025 Ms. Rathi\'s Home Daycare. All rights reserved.</div>
  </footer>

  <script>
    // Hero slider
    let slides=document.querySelectorAll('#heroSlider .hero-slide'),si=0;
    setInterval(()=>{slides[si].classList.remove('active');si=(si+1)%slides.length;slides[si].classList.add('active');},5000);
    // Navbar scroll effect
    window.addEventListener('scroll',()=>{document.getElementById('navbar').classList.toggle('scrolled',window.scrollY>10);});
    // Fade-in on scroll
    let observer=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible');});},{threshold:0.12});
    document.querySelectorAll('.fade-in').forEach(el=>observer.observe(el));
    // Close mobile menu on link click
    document.querySelectorAll('.nav-links a').forEach(a=>a.onclick=()=>document.getElementById('navLinks').classList.remove('open'));
  </script>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
