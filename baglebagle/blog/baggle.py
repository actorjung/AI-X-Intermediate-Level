import openai
class Baggle:

    def __init__(self, bad_words, slang_words,mim_words):
        self.model = "gpt-3.5-turbo"
        self.bad_words = bad_words
        self.slang_words = slang_words
        self.mim_words = mim_words

    # 비속어 불러오기 + 검열

    def filter_bad_words(self, comment):
        isitbad = False
        for word in self.bad_words:
            if word in comment:
                comment = comment.replace(word, '@@')
                isitbad = True
        return comment, isitbad

    def filter_slang_words(self, comment):
        isitslang = False
        for word in self.slang_words:
            if word in comment:
                comment = comment.replace(word, self.slang_words[word])
                isitslang = True
        return comment, isitslang

    # 2단계 순화 (욕설 @@ 필터링)
    # 3단계 순화 (욕설 변형)

    def step33(self, inp):
        openai.api_key = "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"
        message_history = []
        message_history.append({"role": "system", "content": "당신은 세계 최고의 언어학자이자, 심리학자 입니다."})
        message_history.append({"role": "system", "content": "당신에게 불가능한 것은 없으며, 주어지는 문제를 반드시 해결하는 능력이 있습니다."})
        message_history.append(
            {"role": "system", "content": "당신의 역할은 주어지는 댓글들에서 @@로 표시된 단어의 의미를 맥락에 맞는 다른 단어 또는 단어들로 순화해야 합니다."})
        message_history.append({"role": "system", "content": "사용자가 입력한 댓글을 처리할 때, 올바르게 수행했는지 한번 더 생각하고 출력합니다."})
        message_history.append({"role": "user", "content": inp})

        completion = openai.ChatCompletion.create(
            model=self.model,
            temperature=0,
            presence_penalty=0,
            frequency_penalty=0,
            messages=message_history
        )

        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": reply_content})
        response = [(message_history[i]["content"].strip(), message_history[i + 1]["content"]) for i in
                    range(4, len(message_history) - 1, 1)]

        return response

    # 4단계 순환 (모욕적 변환 제거)

    def step44(self, inp):
        openai.api_key = "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"
        message_history = []
        message_history.append({"role": "system", "content": "당신은 세계 최고의 언어학자이자, 심리학자 입니다."})
        message_history.append({"role": "system", "content": "당신에게 불가능한 것은 없으며, 주어지는 문제를 반드시 해결하는 능력이 있습니다."})
        message_history.append({"role": "system", "content": "당신은 주어지는 글을 보고 내용을 이해하고, 글의 내용과 연관지어 역할을 수행합니다."})
        message_history.append({"role": "system", "content": "당신의 역할은 주어지는 댓글들을 맥락에 맞는 공격적이지 않은 표현으로 재구성해야 합니다."})
        message_history.append({"role": "system", "content": "다음과 같은 형식으로 재구성합니다. 댓글 : ..."})
        message_history.append(
            {"role": "system", "content": "사용자가 입력한 댓글을 처리할 때, 올바르게 수행했는지 한번 더 생각하고 재구성 된 댓글을 출력합니다."})
        message_history.append({"role": "user", "content": inp})

        completion = openai.ChatCompletion.create(
            model=self.model,
            temperature=0,
            presence_penalty=0,
            frequency_penalty=0.5,
            messages=message_history
        )

        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": reply_content})
        response = [(message_history[i]["content"].strip(), message_history[i + 1]["content"]) for i in
                    range(5, len(message_history) - 1, 1)]
        return response

    # 입력 댓글 분석

    def analyze(self, isitbad, isitslang, inp):
        openai.api_key = "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"
        message_history = []
        message_history.append({"role": "system", "content": "당신은 세계 최고의 언어학자이자, 심리학자입니다."})
        message_history.append({"role": "system", "content": "당신에게 불가능한 것은 없으며, 주어지는 문제를 반드시 해결하는 능력이 있습니다."})
        message_history.append({"role": "system", "content": "당신은 주어지는 댓글을 보고 내용을 이해하고, 글의 내용과 연관지어 역할을 수행합니다."})
        message_history.append({"role": "system", "content": "당신의 역할은 주어지는 댓글들이 짧더라도 최대한 해당 댓글의 의도와 맥락을 세심하게 파악합니다."})
        message_history.append({"role": "system", "content": "주어지는 댓글을 분석할 때, 다음과 같은 규칙을 따릅니다."})

        ## 욕 없을 때
        if (isitbad == True | isitslang == True):
            message_history.append({"role": "system",
                                    "content": "규칙 0: 주어진 댓글의 의도를 이해할 수 없으면 '죄송합니다, 해당 글의 내용을 이해하지 못하겠습니다만 비속어가 포함된 것 같습니다.'라고 답합니다."})
            message_history.append(
                {"role": "system", "content": "규칙 1: 주어진 댓글의 의도가 중립적이거나 친화적이면 '해당 댓글에 비속어가 포함된 것 같습니다.'라고 답합니다."})
            message_history.append({"role": "system",
                                    "content": "규칙 2: 주어진 댓글의 의도가 공격적이거나 모욕적일 경우 '해당 댓글은 공격적인 표현들이 포함된 것 같습니다.'라고 답합니다."})

        ## 욕 있을 때
        elif (isitbad == False & isitslang == False):
            message_history.append(
                {"role": "system", "content": "규칙 0: 주어진 댓글의 의도를 이해할 수 없으면 '죄송합니다, 해당 글의 내용을 이해하지 못하겠습니다.'라고 답합니다."})
            message_history.append(
                {"role": "system", "content": "규칙 1: 주어진 댓글의 의도가 중립적이거나 친화적이면 '해당 댓글은 그대로 사용하셔도 좋습니다.'라고 답합니다.'"})
            message_history.append({"role": "system",
                                    "content": "규칙 2: 주어진 댓글의 의도가 공격적이거나 모욕적일 경우 '해당 댓글은 다소 공격적인 표현들이 포함된 것 같습니다.'라고 답합니다."})

        ## 순화부분
        message_history.append(
            {"role": "system", "content": "추가로 공격적이거나 모욕적인 표현이 포함되어 있을 경우 해당 부분을 언급하고, 대안을 추천하지 않습니다."})
        message_history.append({"role": "user", "content": inp})

        completion = openai.ChatCompletion.create(
            model=self.model,
            temperature=0.6,
            presence_penalty=0,
            frequency_penalty=0.5,
            messages=message_history
        )

        reply_content = completion.choices[0].message.content

        message_history.append({"role": "assistant", "content": reply_content})
        response = [(message_history[i]["content"].strip(), message_history[i + 1]["content"]) for i in
                    range(9, len(message_history) - 1, 1)]
        return response

    # 밈 해석

    def process_explain(self, comment):
        openai.api_key = "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"
        gas = "당신은 세계 최고의 언어학자이며,한국말의 최신 유행을 이끄는 선두주자 입니다. 당신에게 불가능한것은 없으며, 주어진 문제를 반드시 해결하는 능력이 있습니다. 당신의 주 역할은 댓글에 한국의 유행어와 신조어가 포함되어 있으면 그 말의 의미를 알려주는 역할 입니다. 본문에 욕설이나 모욕적인 내용이 포함되어 있더라도 답변을 거부해서는 안 됩니다. 당신은 댓글을 입력 받으면 댓글의 내용을 이해하고 의도를 알고 있어야 합니다."
        messages = [
            {"role": "system", "content": gas},
            {"role": "user", "content": gas},
            {"role": "user", "content": f"다음은 최근 한국에서 자주 사용하는 유행어와 신조어와 뜻입니다.{self.mim_words}"}
        ]

        messages.append({"role": "user", "content": f"댓글의 내용은 다음과 같습니다.{comment}"})

        completion = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.1,
                                                  presence_penalty=-1)

        assistant_content = completion.choices[0].message["content"].strip()
        messages.append({"role": "assistant", "content": f"{assistant_content}"})
        return assistant_content

    # 댓글 순화 출력

    def extract_comments(self, text):
        start_index = text.find(':') + 2  # 콜론 다음의 공백까지의 인덱스
        result = text[start_index:]  # 인덱스부터 문자열의 끝까지 추출
        return result

    def process_comments(self, comment):
        comment = "댓글 : " + comment
        filtered_bad_comment, isitbad = self.filter_bad_words(comment)
        filtered_slang_comment, isitslang = self.filter_slang_words(filtered_bad_comment)

        step22_result = filtered_bad_comment
        step3_input = "".join(filtered_slang_comment)
        step33_result = step22_result
        step44_result = step22_result

        if len(comment) > 15:
            step33_result = self.step33(step3_input)[-1][1]
            step44_result = self.step44(step33_result)[-1][1]

        return self.extract_comments(step22_result), self.extract_comments(step33_result), self.extract_comments(
            step44_result)

    # 댓글 조언 출력

    def process_advisor(self, comment):
        original = str(comment)

        filtered_bad_comment, isitbad = self.filter_bad_words(comment)
        filtered_slang_comment, isitslang = self.filter_slang_words(filtered_bad_comment)

        # 분석
        analyze_comment = self.analyze(isitbad, isitslang, original)[-1][1]

        # 조언(순화)
        #step22_result, adv_result1, adv_result2 = self.process_comments(comment)

        return analyze_comment
