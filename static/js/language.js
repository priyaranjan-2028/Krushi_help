(function () {
    const storageKey = 'krushi_language';

    const translations = {
        en: {
            lang_label: 'Language',
            nav_about: 'About',
            nav_features: 'Features',
            nav_market: 'Market',
            nav_terms: 'Terms',
            hero_badge: 'Direct Market Access',
            hero_title_html: 'Fair Prices for <span class="highlight-text">Farmers</span>.<br>Fresh Produce for <span class="highlight-text">Buyers</span>.',
            hero_desc: 'Krushi Settu is a smart marketplace that connects farmers directly with buyers. Stop losing money to middlemen and start growing your profits today.',
            hero_farmer_btn: 'I am a Farmer',
            hero_buyer_btn: 'I am a Buyer',
            about_title: 'Why Choose Krushi Settu?',
            about_desc: 'We solve the biggest problem in agriculture: the middleman.',
            old_way_title: 'The Old Way',
            old_way_1: 'Middlemen take huge commissions',
            old_way_2: 'Farmers get low prices',
            old_way_3: 'Buyers pay high retail prices',
            old_way_4: 'Transport issues and wastage',
            new_way_title: 'The Krushi Settu Way',
            new_way_1: '0% Middleman commission',
            new_way_2: 'Farmers set their own fair price',
            new_way_3: 'Buyers get fresh, cheaper produce',
            new_way_4: 'Direct matching reduces cost',
            features_title: 'Powerful Platform Features',
            features_desc: 'Everything you need to buy and sell agricultural products effortlessly.',
            market_title: 'Live Marketplace Sneak Peek',
            market_desc: 'Browse some of the fresh produce listed directly by farmers today.',
            view_all_products: 'View All Products',
            buy_now: 'Buy Now',
            footer_platform: 'Platform',
            footer_company: 'Company',
            footer_farmers: 'For Farmers',
            footer_buyers: 'For Buyers',
            footer_prices: 'Market Prices',
            footer_about: 'About Us',
            footer_contact: 'Contact Support',
            footer_terms: 'Terms and Conditions',
            footer_tagline: 'Empowering farmers by connecting them directly with buyers. Fair prices, better livelihoods.',
            footer_made: 'Made for Farmers',
            back_home: 'Back to home',
            simple_flow: 'Simple flow',
            simple_flow_desc: 'Start with basics, verify mobile, then finish the rest without leaving the page.',
            built_trust: 'Built for trust',
            built_trust_desc: 'Verified mobile number and precise location make the marketplace safer and more reliable.',
            form_complete_steps: 'Complete each step below to finish registration.',
            new_account: 'New Account',
            account_access: 'Account Access',
            basic_details: 'Basic Details',
            mobile_verification: 'Mobile Verification',
            complete_profile: 'Complete Profile',
            send_otp: 'Send OTP',
            proceed_step_2: 'Proceed to Step 2',
            verify_otp: 'Verify OTP',
            mobile_verified: 'Mobile number verified successfully.',
            login_help: 'Need help? Use your verified phone number and continue securely.',
            farmer_sidebar_brand: 'Smart Farmer Marketplace',
            buyer_sidebar_brand: 'Buyer Marketplace',
            menu_dashboard: 'Dashboard',
            menu_crops: 'My Crops',
            menu_sell: 'Sell Product',
            menu_orders: 'Orders',
            menu_messages: 'Messages',
            menu_prices: 'Market Prices',
            menu_profile: 'Profile',
            menu_logout: 'Logout',
            menu_marketplace: 'Marketplace',
            menu_buy: 'Buy',
            menu_farmers: 'Farmer Profiles',
            search_farmer_placeholder: 'Search crops, buyers, prices, or orders',
            search_buyer_placeholder: 'Search farmers, crops, places, or prices',
            location_footer: 'Your Location',
            view_map: 'View Map',
            buy_now_float: 'Buy Now',
            explore_market: 'Explore Market',
            sell_crop_float: 'Sell Crop'
        },
        hi: {
            lang_label: 'भाषा',
            nav_about: 'परिचय',
            nav_features: 'विशेषताएं',
            nav_market: 'बाजार',
            nav_terms: 'नियम',
            hero_badge: 'सीधा बाजार संपर्क',
            hero_title_html: 'किसानों के लिए <span class="highlight-text">उचित दाम</span>।<br>खरीदारों के लिए <span class="highlight-text">ताज़ी उपज</span>.',
            hero_desc: 'कृषि सेतु एक स्मार्ट मार्केटप्लेस है जो किसानों को सीधे खरीदारों से जोड़ता है। बिचौलियों से नुकसान रोकिए और अपना लाभ बढ़ाइए।',
            hero_farmer_btn: 'मैं किसान हूँ',
            hero_buyer_btn: 'मैं खरीदार हूँ',
            about_title: 'कृषि सेतु क्यों चुनें?',
            about_desc: 'हम कृषि की सबसे बड़ी समस्या हल करते हैं: बिचौलिया।',
            old_way_title: 'पुराना तरीका',
            old_way_1: 'बिचौलिये भारी कमीशन लेते हैं',
            old_way_2: 'किसानों को कम दाम मिलते हैं',
            old_way_3: 'खरीदार अधिक कीमत चुकाते हैं',
            old_way_4: 'परिवहन समस्या और बर्बादी',
            new_way_title: 'कृषि सेतु तरीका',
            new_way_1: '0% बिचौलिया कमीशन',
            new_way_2: 'किसान अपना उचित दाम खुद तय करते हैं',
            new_way_3: 'खरीदार को ताज़ा और सस्ता माल मिलता है',
            new_way_4: 'सीधा मिलान लागत घटाता है',
            features_title: 'शक्तिशाली प्लेटफॉर्म विशेषताएं',
            features_desc: 'कृषि उत्पादों को आसानी से खरीदने और बेचने के लिए सब कुछ।',
            market_title: 'लाइव मार्केटप्लेस झलक',
            market_desc: 'आज किसानों द्वारा सूचीबद्ध कुछ ताज़ी उपज देखें।',
            view_all_products: 'सभी उत्पाद देखें',
            buy_now: 'अभी खरीदें',
            footer_platform: 'प्लेटफॉर्म',
            footer_company: 'कंपनी',
            footer_farmers: 'किसानों के लिए',
            footer_buyers: 'खरीदारों के लिए',
            footer_prices: 'बाजार भाव',
            footer_about: 'हमारे बारे में',
            footer_contact: 'सहायता संपर्क',
            footer_terms: 'नियम और शर्तें',
            footer_tagline: 'किसानों को सीधे खरीदारों से जोड़कर सशक्त बनाना। उचित दाम, बेहतर जीवन।',
            footer_made: 'किसानों के लिए बनाया गया',
            back_home: 'मुख्य पृष्ठ पर वापस',
            simple_flow: 'सरल प्रक्रिया',
            simple_flow_desc: 'पहले मूल जानकारी दें, मोबाइल सत्यापित करें, फिर बाकी विवरण पूरा करें।',
            built_trust: 'विश्वास के लिए निर्मित',
            built_trust_desc: 'सत्यापित मोबाइल नंबर और सही स्थान बाज़ार को अधिक सुरक्षित बनाते हैं।',
            form_complete_steps: 'पंजीकरण पूरा करने के लिए नीचे दिए गए चरण पूरे करें।',
            new_account: 'नया खाता',
            account_access: 'खाता प्रवेश',
            basic_details: 'मूल विवरण',
            mobile_verification: 'मोबाइल सत्यापन',
            complete_profile: 'प्रोफ़ाइल पूर्ण करें',
            send_otp: 'ओटीपी भेजें',
            proceed_step_2: 'चरण 2 पर जाएं',
            verify_otp: 'ओटीपी सत्यापित करें',
            mobile_verified: 'मोबाइल नंबर सफलतापूर्वक सत्यापित हुआ।',
            login_help: 'मदद चाहिए? अपना सत्यापित फोन नंबर उपयोग करें और सुरक्षित रूप से आगे बढ़ें।',
            farmer_sidebar_brand: 'स्मार्ट किसान मार्केटप्लेस',
            buyer_sidebar_brand: 'खरीदार मार्केटप्लेस',
            menu_dashboard: 'डैशबोर्ड',
            menu_crops: 'मेरी फसलें',
            menu_sell: 'उत्पाद बेचें',
            menu_orders: 'ऑर्डर',
            menu_messages: 'संदेश',
            menu_prices: 'बाजार भाव',
            menu_profile: 'प्रोफ़ाइल',
            menu_logout: 'लॉगआउट',
            menu_marketplace: 'मार्केटप्लेस',
            menu_buy: 'खरीदें',
            menu_farmers: 'किसान प्रोफ़ाइल',
            search_farmer_placeholder: 'फसलें, खरीदार, भाव या ऑर्डर खोजें',
            search_buyer_placeholder: 'किसान, फसल, स्थान या भाव खोजें',
            location_footer: 'आपका स्थान',
            view_map: 'मानचित्र देखें',
            buy_now_float: 'अभी खरीदें',
            explore_market: 'बाजार देखें',
            sell_crop_float: 'फसल बेचें'
        },
        or: {
            lang_label: 'ଭାଷା',
            nav_about: 'ପରିଚୟ',
            nav_features: 'ବିଶେଷତା',
            nav_market: 'ବଜାର',
            nav_terms: 'ନିୟମ',
            hero_badge: 'ସିଧାସଳଖ ବଜାର ସଂଯୋଗ',
            hero_title_html: '<span class="highlight-text">ଚାଷୀମାନଙ୍କ</span> ପାଇଁ ନ୍ୟାୟସଂଗତ ଦର।<br><span class="highlight-text">କ୍ରେତାମାନଙ୍କ</span> ପାଇଁ ତାଜା ଉତ୍ପାଦ।',
            hero_desc: 'କୃଷି ସେତୁ ହେଉଛି ଏକ ସ୍ମାର୍ଟ ମାର୍କେଟପ୍ଲେସ୍ ଯାହା ଚାଷୀମାନଙ୍କୁ ସିଧାସଳଖ କ୍ରେତାଙ୍କ ସହ ଯୋଡ଼େ। ମଧ୍ୟସ୍ଥଙ୍କୁ ହଟାନ୍ତୁ ଏବଂ ଆପଣଙ୍କ ଲାଭ ବଢ଼ାନ୍ତୁ।',
            hero_farmer_btn: 'ମୁଁ ଚାଷୀ',
            hero_buyer_btn: 'ମୁଁ କ୍ରେତା',
            about_title: 'କୃଷି ସେତୁ କାହିଁକି ବାଛିବେ?',
            about_desc: 'ଆମେ କୃଷିର ସବୁଠୁ ବଡ଼ ସମସ୍ୟାର ସମାଧାନ କରୁଛୁ: ମଧ୍ୟସ୍ଥ।',
            old_way_title: 'ପୁରୁଣା ପ୍ରଣାଳୀ',
            old_way_1: 'ମଧ୍ୟସ୍ଥ ଅଧିକ କମିଶନ୍ ନିଅନ୍ତି',
            old_way_2: 'ଚାଷୀମାନେ କମ ଦର ପାଆନ୍ତି',
            old_way_3: 'କ୍ରେତାମାନେ ଅଧିକ ଦର ଦେଅନ୍ତି',
            old_way_4: 'ପରିବହନ ସମସ୍ୟା ଏବଂ ନଷ୍ଟ',
            new_way_title: 'କୃଷି ସେତୁ ପ୍ରଣାଳୀ',
            new_way_1: '0% ମଧ୍ୟସ୍ଥ କମିଶନ୍',
            new_way_2: 'ଚାଷୀ ନିଜେ ନ୍ୟାୟସଂଗତ ଦର ଧରନ୍ତି',
            new_way_3: 'କ୍ରେତାମାନେ ତାଜା ଏବଂ ସସ୍ତା ଉତ୍ପାଦ ପାଆନ୍ତି',
            new_way_4: 'ସିଧାସଳଖ ମ୍ୟାଚିଂ ଖର୍ଚ୍ଚ କମାଏ',
            features_title: 'ଶକ୍ତିଶାଳୀ ପ୍ଲାଟଫର୍ମ ବିଶେଷତା',
            features_desc: 'କୃଷି ଉତ୍ପାଦ କିଣିବା ଓ ବେଚିବା ପାଇଁ ଆପଣଙ୍କୁ ଦରକାର ସବୁକିଛି।',
            market_title: 'ଲାଇଭ୍ ମାର୍କେଟପ୍ଲେସ୍ ଝଲକ',
            market_desc: 'ଆଜି ଚାଷୀମାନଙ୍କ ଦ୍ୱାରା ତାଲିକାଭୁକ୍ତ କିଛି ତାଜା ଉତ୍ପାଦ ଦେଖନ୍ତୁ।',
            view_all_products: 'ସମସ୍ତ ଉତ୍ପାଦ ଦେଖନ୍ତୁ',
            buy_now: 'ଏବେ କିଣନ୍ତୁ',
            footer_platform: 'ପ୍ଲାଟଫର୍ମ',
            footer_company: 'କମ୍ପାନୀ',
            footer_farmers: 'ଚାଷୀଙ୍କ ପାଇଁ',
            footer_buyers: 'କ୍ରେତାଙ୍କ ପାଇଁ',
            footer_prices: 'ବଜାର ଦର',
            footer_about: 'ଆମ ବିଷୟରେ',
            footer_contact: 'ସହାୟତା ସମ୍ପର୍କ',
            footer_terms: 'ନିୟମ ଓ ଶର୍ତ୍ତ',
            footer_tagline: 'ଚାଷୀମାନଙ୍କୁ ସିଧାସଳଖ କ୍ରେତାଙ୍କ ସହ ଯୋଡ଼ି ସଶକ୍ତ କରୁଛୁ। ନ୍ୟାୟସଂଗତ ଦର, ଭଲ ଜୀବନ।',
            footer_made: 'ଚାଷୀଙ୍କ ପାଇଁ ତିଆରି',
            back_home: 'ମୁଖ୍ୟ ପୃଷ୍ଠାକୁ ଫେରନ୍ତୁ',
            simple_flow: 'ସହଜ ପ୍ରକ୍ରିୟା',
            simple_flow_desc: 'ପ୍ରଥମେ ମୌଳିକ ତଥ୍ୟ ଦିଅନ୍ତୁ, ମୋବାଇଲ୍ ସତ୍ୟାପନ କରନ୍ତୁ, ତାପରେ ଅନ୍ୟାନ୍ୟ ତଥ୍ୟ ପୂରଣ କରନ୍ତୁ।',
            built_trust: 'ବିଶ୍ୱାସ ପାଇଁ ନିର୍ମିତ',
            built_trust_desc: 'ସତ୍ୟାପିତ ମୋବାଇଲ୍ ନମ୍ବର ଏବଂ ସଠିକ୍ ଅବସ୍ଥାନ ମାର୍କେଟକୁ ଅଧିକ ସୁରକ୍ଷିତ କରେ।',
            form_complete_steps: 'ନୋଟିକରଣ ଶେଷ କରିବା ପାଇଁ ନିମ୍ନସ୍ଥ ଧାପଗୁଡ଼ିକ ପୂରଣ କରନ୍ତୁ।',
            new_account: 'ନୂଆ ଖାତା',
            account_access: 'ଖାତା ପ୍ରବେଶ',
            basic_details: 'ମୌଳିକ ତଥ୍ୟ',
            mobile_verification: 'ମୋବାଇଲ୍ ସତ୍ୟାପନ',
            complete_profile: 'ପ୍ରୋଫାଇଲ୍ ପୂରା କରନ୍ତୁ',
            send_otp: 'OTP ପଠାନ୍ତୁ',
            proceed_step_2: 'ଧାପ 2 କୁ ଯାଆନ୍ତୁ',
            verify_otp: 'OTP ସତ୍ୟାପନ କରନ୍ତୁ',
            mobile_verified: 'ମୋବାଇଲ୍ ନମ୍ବର ସଫଳତାର ସହ ସତ୍ୟାପିତ ହେଲା।',
            login_help: 'ସହାୟତା ଦରକାର? ସତ୍ୟାପିତ ଫୋନ୍ ନମ୍ବର ବ୍ୟବହାର କରନ୍ତୁ ଏବଂ ସୁରକ୍ଷିତ ଭାବେ ଆଗକୁ ବଢ଼ନ୍ତୁ।',
            farmer_sidebar_brand: 'ସ୍ମାର୍ଟ ଚାଷୀ ମାର୍କେଟପ୍ଲେସ୍',
            buyer_sidebar_brand: 'କ୍ରେତା ମାର୍କେଟପ୍ଲେସ୍',
            menu_dashboard: 'ଡ୍ୟାଶବୋର୍ଡ',
            menu_crops: 'ମୋ ଫସଲ',
            menu_sell: 'ଉତ୍ପାଦ ବେଚନ୍ତୁ',
            menu_orders: 'ଅର୍ଡର',
            menu_messages: 'ସନ୍ଦେଶ',
            menu_prices: 'ବଜାର ଦର',
            menu_profile: 'ପ୍ରୋଫାଇଲ୍',
            menu_logout: 'ଲଗଆଉଟ୍',
            menu_marketplace: 'ମାର୍କେଟପ୍ଲେସ୍',
            menu_buy: 'କିଣନ୍ତୁ',
            menu_farmers: 'ଚାଷୀ ପ୍ରୋଫାଇଲ୍',
            search_farmer_placeholder: 'ଫସଲ, କ୍ରେତା, ଦର କିମ୍ବା ଅର୍ଡର ଖୋଜନ୍ତୁ',
            search_buyer_placeholder: 'ଚାଷୀ, ଫସଲ, ସ୍ଥାନ କିମ୍ବା ଦର ଖୋଜନ୍ତୁ',
            location_footer: 'ଆପଣଙ୍କ ଅବସ୍ଥାନ',
            view_map: 'ମାନଚିତ୍ର ଦେଖନ୍ତୁ',
            buy_now_float: 'ଏବେ କିଣନ୍ତୁ',
            explore_market: 'ବଜାର ଦେଖନ୍ତୁ',
            sell_crop_float: 'ଫସଲ ବେଚନ୍ତୁ'
        }
    };

    function applyLanguage(lang) {
        const selected = translations[lang] ? lang : 'en';
        localStorage.setItem(storageKey, selected);
        document.documentElement.lang = selected;

        document.querySelectorAll('[data-i18n]').forEach((element) => {
            const key = element.dataset.i18n;
            const value = translations[selected][key];
            if (value) {
                element.textContent = value;
            }
        });

        document.querySelectorAll('[data-i18n-html]').forEach((element) => {
            const key = element.dataset.i18nHtml;
            const value = translations[selected][key];
            if (value) {
                element.innerHTML = value;
            }
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
            const key = element.dataset.i18nPlaceholder;
            const value = translations[selected][key];
            if (value) {
                element.setAttribute('placeholder', value);
            }
        });

        document.querySelectorAll('[data-language-select]').forEach((select) => {
            select.value = selected;
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        const initial = localStorage.getItem(storageKey) || 'en';
        applyLanguage(initial);

        document.querySelectorAll('[data-language-select]').forEach((select) => {
            select.addEventListener('change', function () {
                applyLanguage(select.value);
            });
        });
    });
})();
