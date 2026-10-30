import time
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from PIL import Image
from transformers import pipeline

print("Initializing CortexVision Ultimate Matrix Engine...")

try:
    ai_engine = pipeline("image-classification", model="microsoft/resnet-50")
    print("CortexVision Neural Core is 100% ONLINE! 🚀")
except Exception as e:
    print(f"Core Activation Error: {e}")
    ai_engine = None


def login_view(request):
    error_msg = None
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            return render(request, 'upload.html', {'show_welcome': True})
        else:
            error_msg = "رمز ورود یا نام کاربری اشتباه است."
            
    return render(request, 'login.html', {'error_msg': error_msg})


def image_upload_view(request):
    if request.method == 'POST' and request.FILES.get('user_image'):
        uploaded_file = request.FILES['user_image']

        try:
            img = Image.open(uploaded_file)
            start_time = time.time()
            
            if ai_engine:
                predictions = ai_engine(img, top_k=10)
                

                cat_signals = ['cat', 'tabby', 'siamese', 'persian', 'lynx', 'tiger cat']
                dog_signals = ['dog', 'terrier', 'retriever', 'shepherd', 'husky', 'poodle', 'pug']
                bird_signals = ['bird', 'macaw', 'robin', 'eagle', 'parrot', 'penguin']
                fish_signals = ['fish', 'goldfish', 'shark', 'lionfish']
                car_signals = ['car', 'sports car', 'racer', 'convertible', 'limousine', 'cab', 'jeep', 'minivan', 'truck', 'ambulance', 'vehicle']
                bug_signals = ['butterfly', 'bee', 'insect', 'spider', 'ant', 'fly', 'cricket', 'beetle', 'grasshopper', 'dragonfly', 'cockroach', 'tick']

                dino_signals = ['dinosaur', 'fossil', 'trilobite', 'archaeopteryx', 'skeleton', 'bone', 'crocodile', 'alligator', 'lizard', 'frilled lizard']
                
                chair_signals = ['chair', 'folding chair', 'barber chair', 'rocking chair', 'armchair']
                table_signals = ['table', 'desk', 'dining table', 'coffee table', 'pool table']
                lamp_signals = ['lamp', 'table lamp', 'floor lamp', 'lantern', 'light']
                furniture_signals = ['couch', 'studio couch', 'sofa', 'wardrobe', 'cabinet', 'bookcase']

                human_keywords = ['abaya', 'gown', 'skirt', 'miniskirt', 'wig', 'hair slide', 'apron', 'jersey', 'suit', 'tie', 't-shirt', 'jacket', 'jeans']
                
                top_asset = predictions[0]['label'].split(',')[0].title()
                top_confidence = round(predictions[0]['score'] * 100, 1)
                
                entity_type = "موجودیت فیزیکی (Static Object)"
                sub_analysis_html = ""
                matched_category = None
                type_fa = ""

                for pred in predictions:
                    label_lower = pred['label'].lower()
                    
                    if any(c in label_lower for c in cat_signals):
                        matched_category = "animal"; type_fa = "گربه 🐱"; break
                    elif any(d in label_lower for d in dog_signals):
                        matched_category = "animal"; type_fa = "سگ 🐶"; break
                    elif any(b in label_lower for b in bird_signals):
                        matched_category = "animal"; type_fa = "پرنده 🦜"; break
                    elif any(f in label_lower for f in fish_signals):
                        matched_category = "animal"; type_fa = "ماهی 🐟"; break
                    elif any(bug in label_lower for bug in bug_signals):
                        matched_category = "animal"; type_fa = "حشره / بندپا 🦋"; break
                    elif any(car in label_lower for car in car_signals):
                        matched_category = "vehicle"; type_fa = "خودرو / وسیله نقلیه 🚗"; break
                    elif any(dino in label_lower for dino in dino_signals):
                        matched_category = "dino"; type_fa = "آثار باستانی / دایناسور 🦖"; break
                    elif any(ch in label_lower for ch in chair_signals):
                        matched_category = "furniture"; type_fa = "صندلی / نشیمن 🪑"; break
                    elif any(tb in label_lower for tb in table_signals):
                        matched_category = "furniture"; type_fa = "میز / سطح کار 🪵"; break
                    elif any(lp in label_lower for lp in lamp_signals):
                        matched_category = "furniture"; type_fa = "تجهیزات روشنایی / لامپ 💡"; break
                    elif any(fr in label_lower for fr in furniture_signals):
                        matched_category = "furniture"; type_fa = "مبلمان و دکوراسیون 🛋️"; break
                    elif any(hum in label_lower for hum in human_keywords):
                        matched_category = "human"; break

                if matched_category == "animal":
                    entity_type = "جاندار / حیوان (Animal)"
                    sub_analysis_html = f'''
                        <div style="background: rgba(46, 204, 113, 0.05); border: 1px solid rgba(46, 204, 113, 0.2); padding: 14px; border-radius: 14px; margin-bottom: 20px; text-align: right;">
                            <span style="color: #2ecc71; font-size: 10px; font-weight: 700; display: block; margin-bottom: 6px;">هسته بیولوژیکی سیستم</span>
                            <span style="color: #ffffff; font-size: 15px; font-weight: 600; display: block;">🐾 تشخیص گونه: {type_fa}</span>
                            <span style="color: #2ecc71; font-size: 13px; font-weight: 500; display: block; margin-top: 4px;">📊 نژاد فیزیکی: {top_asset} ({top_confidence}٪)</span>
                        </div>
                    '''
                elif matched_category == "vehicle":
                    entity_type = "وسایل نقلیه (Vehicle)"
                    sub_analysis_html = f'''
                        <div style="background: rgba(155, 89, 182, 0.05); border: 1px solid rgba(155, 89, 182, 0.2); padding: 14px; border-radius: 14px; margin-bottom: 20px; text-align: right;">
                            <span style="color: #9b59b6; font-size: 10px; font-weight: 700; display: block; margin-bottom: 6px;">ماتریس حمل و نقل کورتکس</span>
                            <span style="color: #ffffff; font-size: 15px; font-weight: 600; display: block;">🚘 دسته‌بندی: {type_fa}</span>
                            <span style="color: #9b59b6; font-weight: 500; display: block; margin-top: 4px;">📊 مدل دقیق: {top_asset} ({top_confidence}٪)</span>
                        </div>
                    '''
                elif matched_category == "dino":
                    entity_type = "پالئونتولوژی / باستان‌شناسی"
                    display_asset = "Prehistoric Reptile / T-Rex" if "crocod" in top_asset.lower() or "lizard" in top_asset.lower() else top_asset
                    sub_analysis_html = f'''
                        <div style="background: rgba(230, 126, 34, 0.05); border: 1px solid rgba(230, 126, 34, 0.2); padding: 14px; border-radius: 14px; margin-bottom: 20px; text-align: right;">
                            <span style="color: #e67e22; font-size: 10px; font-weight: 700; display: block; margin-bottom: 6px;">هسته تاریخ طبیعی و فسیل‌شناسی</span>
                            <span style="color: #ffffff; font-size: 15px; font-weight: 600; display: block;">🦖 تحلیل بافت: {type_fa}</span>
                            <span style="color: #e67e22; font-size: 13px; font-weight: 500; display: block; margin-top: 4px;">📊 تشابه ساختاری: {display_asset} ({top_confidence}٪)</span>
                        </div>
                    '''
                elif matched_category == "furniture":
                    entity_type = "دکوراسیون / تجهیزات محیطی"
                    sub_analysis_html = f'''
                        <div style="background: rgba(52, 152, 219, 0.05); border: 1px solid rgba(52, 152, 219, 0.2); padding: 14px; border-radius: 14px; margin-bottom: 20px; text-align: right;">
                            <span style="color: #3498db; font-size: 10px; font-weight: 700; display: block; margin-bottom: 6px;">آنالیز دکوراسیون و اشیاء فیزیکی</span>
                            <span style="color: #ffffff; font-size: 15px; font-weight: 600; display: block;">🛋️ نوع شیء: {type_fa}</span>
                            <span style="color: #3498db; font-size: 13px; font-weight: 500; display: block; margin-top: 4px;">📊 تطبیق ساختار: {top_asset} ({top_confidence}٪)</span>
                        </div>
                    '''
                elif matched_category == "human":
                    entity_type = "موجودیت انسان (Human)"
                    detected_gender = "زن (Female)" if any(sig in predictions[0]['label'].lower() or sig in predictions[1]['label'].lower() for sig in ['abaya', 'gown', 'skirt', 'jersey']) else "مرد (Male)"
                    sub_analysis_html = f'''
                        <div style="background: rgba(10, 132, 255, 0.05); border: 1px solid rgba(10, 132, 255, 0.2); padding: 14px; border-radius: 14px; margin-bottom: 20px; text-align: right;">
                            <span style="color: #0a84ff; font-size: 10px; font-weight: 700; display: block; margin-bottom: 6px;">تحلیل دموگرافیک فرد</span>
                            <span style="color: #ffffff; font-size: 15px; font-weight: 600; display: block;">👤 هویت فیزیکی: {detected_gender}</span>
                            <span style="color: #0a84ff; font-size: 13px; font-weight: 500; display: block; margin-top: 4px;">🎯 وضعیت رادار: کاملاً پایدار</span>
                        </div>
                    '''
                else:
                    sub_analysis_html = f'''
                        <div style="background: rgba(255, 159, 10, 0.05); border: 1px solid rgba(255, 159, 10, 0.2); padding: 14px; border-radius: 14px; margin-bottom: 20px; text-align: right;">
                            <span style="color: #ff9f0a; font-size: 10px; font-weight: 700; display: block; margin-bottom: 6px;">هسته متریال و دارایی‌ها</span>
                            <span style="color: #ffffff; font-size: 15px; font-weight: 600; display: block;">📦 شیء شناسایی‌شده: {top_asset}</span>
                            <span style="color: #ff9f0a; font-size: 13px; font-weight: 500; display: block; margin-top: 4px;">📊 میزان دقت تطبیق: {top_confidence}٪</span>
                        </div>
                    '''

                object_list_html = ""
                for pred in predictions[:3]:
                    object_list_html += f'''
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 6px; display: flex; justify-content: space-between; direction: ltr;">
                            <span style="color: #ffffff; font-size: 14px;">🔹 {pred['label'].split(',')[0]}</span>
                            <span style="color: #a1a1a6; font-size: 13px;">{round(pred['score'] * 100, 1)}%</span>
                        </div>
                    '''
            else:
                object_list_html = '<div>هسته آفلاین است</div>'
                sub_analysis_html = '<div>خطای موتور</div>'

            end_time = time.time()
            latency = round((end_time - start_time) * 1000)

        except Exception as e:
            object_list_html = f"خطا: {str(e)}"
            sub_analysis_html = "خطای پردازش"
            latency = 0

        return HttpResponse(f'''
            <body style="font-family: -apple-system, sans-serif; background-color: #000000; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; direction: rtl;">
                <div style="background: #1c1c1e; padding: 35px; border-radius: 24px; border: 1px solid rgba(255,255,255,0.08); text-align: center; width: 360px; box-shadow: 0 25px 50px rgba(0,0,0,0.5);">
                    <h3 style="color: #ffffff; margin-bottom: 5px; font-weight: 600; font-size: 20px;">تحلیل ماتریکس کامل شد</h3>
                    <p style="color: #8e8e93; font-size: 12px; margin-bottom: 25px;">تاخیر سخت‌افزار: <span style="color: #0a84ff; font-weight: 600; direction: ltr; display: inline-block;">{latency} ms</span></p>
                    
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; text-align: right; margin-bottom: 15px;">
                        <span style="color: #8e8e93; font-size: 9px; font-weight: 700; display: block; margin-bottom: 4px;">متاکلاس دسته‌بندی ماهیت</span>
                        <span style="color: #ffffff; font-size: 15px; font-weight: 600;">🔮 ماهیت تصویر: {entity_type}</span>
                    </div>

                    {sub_analysis_html}

                    <div style="text-align: right; margin-bottom: 25px;">
                        <span style="color: #8e8e93; font-size: 10px; font-weight: 700; display: block; margin-bottom: 10px;">ویژگی‌های ساختاری اطراف شیء</span>
                        {object_list_html}
                    </div>
                    <a href="/upload/" style="display: inline-block; width: 100%; padding: 14px 0; background: #0a84ff; color: white; text-decoration: none; border-radius: 12px; font-weight: 600; box-sizing: border-box; font-size: 15px;">تحلیل تصویر جدید</a>
                </div>
            </body>
        ''')
    
    return render(request, 'upload.html')