import os
import google.generativeai as genai
from tqdm import tqdm
from utils import ConfigLoader
from preprocess import preprocess_text
    
def initialize_model():
    """
    yotube 영상 분류 프롬프트가 작성된 gemini 모델 불러오기
    """
    config = ConfigLoader("config.json")
    config.load()
    gemini_key = config.get("gemini_key")
    genai.configure(api_key=gemini_key)
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
        system_instruction="주어진 유튜브 영상 제목과 영상 설명이 뷰티(화장품) 브랜드와 관련이 있는지 또는 없는지 분류해주세요. 관련이 있을 경우 1, 없을 경우 0으로 알려주세요.\n\ninput: [🧥코트 25벌 버려본 여자의 지금 사면 10년 입는 코트 8벌 추천🧡 소재,핏,디자인,가격,퀄리티 빠지는 거 없는 30만원 이하 코트🧵 지에마르, 리리수, 엣드맹, OER, 베르봄]이 영상은 유료광고를 포함하지 않습니다.\\n* 할인은 제가 직접 브랜드 컨택 후 설득을 통해 요청드리고 설득한 할인들입니다! :) \\n* 여러분 안녕하세요. 또 저예요. 세 번째 제품 추천 시리즈네요. 이번엔 코트입니다. 코트가 참 비싸잖아요. 그래서 사실 다른 옷보다 하나 구매할 때 더 더 신중하게 되는 것 같아요. 색상 선택도 정말 어렵고요. 저는 20대 초반에는 다양한 디자인의 옷을 “많이” 가지고 싶어서 저렴한 코트들을 참 많이 샀었어요. 아쉽게도 그때 산 옷 중에 아직 제 드레스룸에 남아있는 옷은 없습니다 ㅎㅎ 많은 시행 착오를 거치며 코트는 ‘좋은 걸 하나 사서 오래입자’ ‘일년에 한두개씩 모아가자’ 이렇게 생각하게 된 것 같아요. 이번 영상은 일부러 핏, 길이, 컬러, 소재 등등 다양하게 구성해봤는데 도움이 되었으면 좋겠습니다.\\n* 기재된 링크를 통해 발생한 수익의 일부를 지급 받을 수 있습니다.\\n* 키 1567cm / 몸무게 - 4344kg\\n\\n1. 🧥GIEMAR - 38% 할인🔥 (02:09) \\nCOLLAR POINT WOOL LONG COAT BEIGE 카라 포인트 울 롱 코트🧥\\n(정가) 306,000원 - (최종가) 198,000원\\n* 비슷비슷한 코트 디자인으로 피로해진 와중에 한 눈에 들어왔던 코트입니다.\\n* 볼륨감이 느껴지는 넥라인이 너무 예쁜 코트예요. \\n* 프리사이즈인데 제게는 조금 크고 길어서 저는 수선할 생각이에요. 저보다 키가 좀 더 있으신 분들은 더욱 멋지게 소화하실 수 있을 것 같아요!\\n* 베이지 - https://zvzo.xyz/@januaryoonzi/e/EIdEknFHCoSW45TxJm3RmWw/p/PAxgKXReuepJo/\\n* 그레이 - https://zvzo.xyz/ko/@januaryoonzi/e/EIdEknFHCoSW45TxJm3RmWw/p/PA9twy7CY-qb4/?type=BRAND\\n\\n\\n2. 🧥OER - 22% 할인🔥 (03:57)\\n울 캐시미어 싱글 코트\\n(정가) 358,000원 - (최종가) 279,240원\\n* 가장 베이직한 기본 코트를 찾는다면 저는 이 코트를 추천하고 싶어요! \\n* 군더더기를 찾아볼 수 없는 디자인에다가 일자로 똑 떨어지는 핏이 너무 멋있는 코트예요.\\n* 그리고 캐시미어가 들어가있어서 코트가 정말 부드러워요. 코트 만져보면 소재 좋다는 것을 바로 알 수 있음!\\n* 테일러링이 엄청 정교해서 개인적으로는 ‘잘 만들어진 수트’를 보는 느낌이었어요!\\n* 블랙 - https://zvzo.xyz/@januaryoonzi/e/EQ8jSwawKqEFf6znjlGt1JA/p/PA5pzuFl_vCUk/\\n* 챠콜 - https://zvzo.xyz/@januaryoonzi/e/EQ8jSwawKqEFf6znjlGt1JA/p/PAb2fL14-RFSY/\\n\\n3. 🧥ET demain - 40% 할인🔥 (05:33)\\nCaraibi alpaca-blend half coat (Ivory)\\n(정가) 335,000원- (최종가) 201,000원\\n* 작년에 구매해서 너무 잘입고 있는 코트예요. \\n* 저는 키가 작은 편이라 늘 코트 기장이 어려운데 하프코트라 너무 길지도 짧지도 않아서 활용도가 높아요.\\n* 엉덩이는 덮으면서도 허벅지를 너무 덮지 않아 키가 커보이는 효과! \\n* 작년에는 스커트나 반바지와 자주 입었는데 올해는 또 캐쥬얼한 룩으로 자꾸 입게 되네요. 실물이 더 예뿐 코트라 강추합니다\\n* 아이보리 - https://zvzo.xyz/@januaryoonzi/e/EB2tOFu6_uFXk9sG6Tf_RQg/p/PALJUS-tFJsmI/\\n* 핑크 - https://zvzo.xyz/@januaryoonzi/e/EB2tOFu6_uFXk9sG6Tf_RQg/p/PAetGNbby4qUA/\\n\\n🧶구독자 이벤트🧶 \\n* 구매하신 분들은 제 인스타그램과(@januaryoonzi) 엣드맹 인스타그램 (@etdemain_official) 을 태그하여 스토리에 인증해주세요!\\n* 추첨을 통해 다섯 분께 LOGO-PRINT EMBROIDERED JERSEY SWEATSHIRT (BLACK)을 보내드릴게요!\\n\\n4. 🧥 LILISU - 45% 할인 🔥 (07:24)\\nEmma Coat (2Color)\\n(정가) 565,200원 - (최종가) 304,722 원\\n* 유치한 느낌이 없는 더플코트를 찾아 몇년 째 헤매던 제가 보자마자 ‘이거다!’ 했던 코트입니다.\\n* 배송와서 입어보니 너무 예뻐서 정말 감탄에 감탄을 했던 코트예요! 리리수를 소개하기로 결심한 이유가 되었던 코트!\\n* 자칫하면 둔해보일 수 있는 더플코트를 어쩜 이렇게 슬림하고 깔끔하게 뽑아내었는지 너무 맘에 듭니다.\\n* 코코아 컬러인데 밝은 편이라 오히려 얼굴이 환해보여요!\\n* 저는 올해 들인 코트 중 가장 만족하는 코트라 정말 강추해요\\n* 2color - https://zvzo.xyz/@januaryoonzi/e/EECNAB6QYRqUVGwj_Veqa_g/p/PAGE8hZVruKvA/\\n\\n5. 🧥 LILISU - 45% 할인 🔥 (09:37)\\nSimone Coat / Camel\\n(정가) 439,100원 - (최종가) 238,000원\\n* 저는 약간 박시한 카멜 코트는 있는데 정핏으로 똑 떨어지는 코트가 없어서 그런 코트를 내내 찾았는데요, 요겁니다!\\n* 제 상상 속 멋쟁아 커리어우먼은 얇은 블랙 니트에 블랙 슬랙스를 입고 요런 코트를 딱 ! 걸쳐준 이미지였어요.\\n* 허리 끈이 없지만 코트 자체에 라인이 잡혀있어서 정말 날씬해보이고 촤르르 떨어지는 핏이 예술입니다.\\n* 그리고 소재! 윤기와 광나는 소재… 실물이 훨씬 고급스러워요!\\n* 카멜 - https://zvzo.xyz/@januaryoonzi/e/EKDL_zmHXTL0zKMxhCRB3RA/p/PAsy11P4Dlu8Q/\\n\\n6. 🧥 VERBOM - 45% 할인 🔥(11:04)\\n[ 3rd ] Reversible Suede Mustang_Brown\\n(정가) 370,000원 - (최종가) 277,500원\\n* 소재와 디테일로 승부를 보는 무스탕이라고 생각합니다. 무스탕의 결과 윤기가 살아 있어요! \\n* 비슷한 디자인의 저렴한 무스탕이랑은 퀄리티 차이가 너무 많이 납니다!\\n* 영상에서도 설명했지만 말로만 리버서블인 옷들이 너무 많은데 이건 어떤 유형이 기본 유형인지 모를 정도로 완벽하게 만들어졌어요. 심지어 전 리버서블 버전으로 훨씬 많이 입음!\\n* 아우터 하나의 가격으로 완전한 두가지 아우터를 산 느낌이라 받아보면 무조건 만족할 수 밖에 없는 옷이라고 자신해요 ㅎㅎ\\n* 브라운 - https://zvzo.xyz/@januaryoonzi/e/E7r9DNX8ywFGrTq1oytNADA/p/PAZU6Qd4kejpk/\\n\\n7. 🧥 LILISU - 41% 할인 🔥(13:16)\\nDori Coat / Black\\n(정가) 450,340원 - (최종가) 278,000원\\n* 이 코트는 사실 리리수 구경하며 제일 먼저 눈에 들어왔던 코트입니다! 왠지 제게는 클 것 같아 괜히 모험하기 싫은 마음에 패스했던 코트인데 입어보니 너무 예뻐요.\\n* 어떤 코트는 페미닌하고 어떤 코트는 중성적인 매력이 있는데요, 이 코트는 두가지 모두 가능한 코트입니다!\\n* 끈을 매느냐, 안매느냐에 따라 넥라인을 어떻게 연출하느냐에 따라 코트 느낌이 카멜레온처럼 변해요! 소재는 물론 정말 좋고요!\\n* 몇년 째 사랑받는 온고잉 코트라고 해요, 늘 말하지만 대중픽엔 다 이유가 있습니다 ㅎㅎ\\n* 블랙 - https://zvzo.xyz/@januaryoonzi/e/E0gp4Aq_qyN-Fpu5QFJBRGA/p/PAZHOuQqwZzPQ/\\n* 카멜 - https://zvzo.xyz/@januaryoonzi/e/E0gp4Aq_qyN-Fpu5QFJBRGA/p/PALJwsoREQBho/\\n\\n8. 🧥 LILISU - 47% 할인 🔥(15:10)\\nAndy coat - egg\\n(정가) 498,000원 - (최종가) 258,000원\\n* 왜 너무 맘에 들어서 아껴서 입고 싶은 옷 있잖아요. 이게 저한테 그런 코트예요. 여행가는 날 입으려고 아껴두는 코트.\\n* 사실상 제 원픽 코트인데 관리가 힘들다는 이유로 요 색상을 패스하시는 분들이 많을 것 같아 마지막으로 빼게 된 코트입니다!\\n* 부클 느낌 나는 소재 덕분에 캐주얼한 느낌도 나는데 볼륨감 있는 핏 덕분에 페미닌한 느낌도 납니다!\\n* 끈도 없고 단추도 몇개 없는데요. 구조적으로 잘 만들어진 옷이라 아방한 느낌이 너무 예뻐요. 이 코트 입을 때마다 환해보인다는 말을 많이 들었어요! \\n* 화이트 - https://zvzo.xyz/@januaryoonzi/e/EpzowJ7ry2WZ6VtUWZ1-mYA/p/PAHWdykDHypqE/\\n\\n\\n✨Instagram : januaryoonzi \\n✨Editing software : pr. cc 2018 \\n✨Contact : bubblylinda@gmail.com\noutput: 0\n\ninput: [#립밤 #틴트밤 바세린 립테라피 한정판 리뷰 (+ 컬러앤케어 프리티피치&고져스 그레이프프룻)]안녕하세요 리피립스입니당😊\\n이번 리뷰는 바세린 립테라피 리뷰입니당!\\n퀸비랑 핑크버블리는 해외에서만 출시되었던 향인데 국내에 한정으로 판매한다고해서 바로 구매해봤습니다!\\n도움이 되셨길 바라며 구매하고싶으시면 품절되기 전에 얼른 구매하시길 바랍니당!\\n그럼 다음 리뷰영상에서 봬요 안뇽\noutput: 1\n\ninput: [혹시 요정이세요? #김혜윤 #로우퀘스트]#로우퀘스트 #김혜윤 #rawquest #kimhyeyoon\noutput: 0",
    )

    chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "[엘라스틴데스모신   추천   BEST 3  올해 인기상품  3ㅣ추천템ㅣ생활 꿀템ㅣ]영상 속 엘라스틴데스모신 구매링크:\\nhttps://link.coupang.com/a/b3rFTP\\n이 포스팅은 쿠팡파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.\\n\\n1위 : 휴나인 데스모신 엘라스틴 콜라겐 60정, 60정, 4개\\n가격 : 47,700원\\n링크 : https://link.coupang.com/a/b3rFTP\\n\\n2위 : 순수식품 엘라스틴 데스모신 저분자 피쉬 콜라겐 히알루론산 밀크세라마이드\\n가격 : 21,590원\\n링크 : https://link.coupang.com/a/b3rFTS\\n\\n3위 : 순수식품 엘라스틴 데스모신 저분자 피쉬 콜라겐 히알루론산 밀크세라마이드\\n가격 : 49,480원\\n링크 : https://link.coupang.com/a/b3rFTT\\n\\n감사합니다.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "0",
      ],
    },
    {
      "role": "user",
      "parts": [
        "쇼파의 앉아 버블리!!",
      ],
    },
    {
      "role": "model",
      "parts": [
        "0",
      ],
    },
  ]
)

    return chat_session    

def classify_text(chat_session, text):
    """
    initialize_model을 사용하여 주어진 텍스트를 분류합니다.
    
    chat_session: 채팅 세션 객체
    text: 분류할 유튜브 제목과 영상 설명
    return: 분류 결과를 1(뷰티 관련) 또는 0(뷰티와 관련 없음)으로 반환
    """
    text = preprocess_text(text)
    response = chat_session.send_message(text)
    return response.text
