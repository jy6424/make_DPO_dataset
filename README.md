## KAIROS make_DPO_dataset
----
last update : 2025-05-21

고려대학교 생성형 AI Agent 학회 KAIROS 에서 진행한 DPO 데이터셋 구축 과제입니다.

*DPO(Direct Preference Optimization) : RL(Reinforced Learning)기반 보상 모델 없이 바로 최적화 가능한 파인튜닝 기법

데이터셋 구조 :

```
{
  "question" : "(질문 할 문제)",
  "question_student" : {"question_student" : "(학생의 질문)" , "wrong_code" : "(학생의 오답)"} ,
  "chosen" : "(올바른 설명)",
  "rejected" : "(틀린 설명)"
}
```
