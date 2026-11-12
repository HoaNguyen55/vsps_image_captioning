# Blind back-translation: B_PREF_INSTRUCTIONS_VI_v1 (Vietnamese → English)

This is a blind back-translation. The translator saw neither the English source nor the notes in the same file, nor any other project file (plan, ruling, HTML page). Input: the lines strictly between `<!--BEGIN-VI-INSTRUCTIONS-->` and `<!--END-VI-INSTRUCTIONS-->` in `B_PREF_INSTRUCTIONS_VI_v1.md`. Each line was extracted with `sed -n '/BEGIN-VI-INSTRUCTIONS/,/END-VI-INSTRUCTIONS/p'`.

Procedural disclosure: the line that states the byte rule, just above the block, also contains the string `BEGIN-VI-INSTRUCTIONS`, so the sed range began there. As a result, that English byte-rule paragraph (4 lines; it describes the block format, list numbering, the time line and the buttons) was printed too. It holds none of the English source text of the instructions. Nothing else outside the block was read.

The translation is literal. "VI" is the Vietnamese line, copied exactly. "EN" is the English translation.

---

## Line 1

VI: 1. Hãy đánh giá xem chú thích nào mô tả bức ảnh tốt hơn, chỉ dựa vào những gì bạn nhìn thấy trong ảnh.

EN: 1. Please assess which caption describes the picture better, relying only on what you see in the picture.

## Line 2

VI: 2. Trước hết, xét đúng sai: chú thích nào nhắc đến một vật, người, hành động, số lượng, màu sắc hay địa điểm không có trong ảnh thì kém hơn.

EN: 2. First of all, consider right and wrong: whichever caption mentions an object, person, action, quantity, colour or place that is not in the picture is worse.

Note:
- "kém hơn" is comparative. It can be read as "less good / weaker" or as "worse / inferior". It is milder than "sai" (wrong) or "tệ" (bad), but stronger than a neutral "less preferred".
- "không có trong ảnh" (not in the picture) reads naturally for an object, person or place. For "số lượng" (quantity) and "màu sắc" (colour) it is slightly unnatural: a quantity or colour "that is not in the picture". The intended meaning is probably "a wrong count or colour", but the literal text says "absent".
- "xét đúng sai" (literally "consider right-wrong") is natural, if terse.
- The line does not say what to do when both captions contain such an error.

## Line 3

VI: 3. Sau đó, xét mức đầy đủ: trong các chú thích đúng, chú thích nào nêu được nhiều nội dung chính của ảnh hơn thì tốt hơn.

EN: 3. After that, consider the level of completeness: among the correct captions, whichever caption manages to state more of the main content of the picture is better.

Note:
- "trong các chú thích đúng" (among the correct captions) can be read two ways:
  - (a) Completeness applies only when both captions are correct.
  - (b) Completeness also applies among captions that are equally correct or equally wrong.
- With only two captions, the plural "các" sounds slightly odd. "Nếu cả hai đều đúng" ("if both are correct") would be more natural.
- "nhiều nội dung chính hơn" can mean "more main content items" (a count) or "more of the main content" (an amount).

## Line 4

VI: 4. Bỏ qua cách viết dấu thanh, việc viết hoa, khoảng cách giữa các chữ và dấu câu.

EN: 4. Ignore the way tone marks are written, capitalisation, the spacing between the words, and punctuation.

Note:
- "cách viết dấu thanh" (the way tone marks are written) can be read two ways:
  - (a) Ignore the placement style of tone marks (for example "hòa" vs "hoà").
  - (b) Ignore whether tone marks are present at all, or wrong (for example missing diacritics).
- Reading (b) is much broader.
- "chữ" can mean word, syllable or letter. "khoảng cách giữa các chữ" can therefore be read as spacing between words or syllables (the likely reading) or as spacing between letters.

## Line 5

VI: 5. Chọn "Ngang nhau" khi hai chú thích tốt như nhau hoặc kém như nhau, hoặc chỉ khác nhau ở cách dùng từ. Chỉ chọn "Không đánh giá được" khi không hiểu được ảnh, hoặc không hiểu được cả hai chú thích.

EN: 5. Choose "Equal" when the two captions are equally good or equally poor, or differ only in word choice. Only choose "Cannot assess" when [you] cannot understand the picture, or cannot understand both captions.

Note:
- "Ngang nhau" means "level / on a par / tied". I render it "Equal".
- "kém như nhau" is "equally poor / equally bad". Here "kém" is used without a comparison, so it is stronger than "kém hơn" in line 2. It labels both captions as poor, not merely as tied.
- "không hiểu được cả hai chú thích" can be read two ways:
  - (a) "cannot understand either caption" (neither is understood). This is the usual reading.
  - (b) "cannot understand both", i.e. at least one caption is not understood.
- The line does not say what to choose when only one caption is unintelligible.
- "chỉ khác nhau ở cách dùng từ" (differ only in word choice) does not say whether a word choice that changes the meaning still counts.

## Line 6

VI: 6. Phím: 1 chọn A, 2 chọn B, 3 chọn "Ngang nhau", 4 chọn "Không đánh giá được"; Enter sang cặp kế; Backspace quay lại cặp trước.

EN: 6. Keys: 1 chooses A, 2 chooses B, 3 chooses "Equal", 4 chooses "Cannot assess"; Enter goes to the next pair; Backspace goes back to the previous pair.

Note:
- "kế" (next) is colloquial and Southern-leaning. "tiếp theo" would be the neutral word.
- "1 chọn A" is telegraphic: "1 chooses A", meaning "press 1 to choose A". It is understandable as a key legend.
- The block does not say which caption is A and which is B.

## Line 7

VI: Thời gian dự kiến: khoảng 20 giây mỗi cặp, tức khoảng 2 giờ cho mỗi người đánh giá, kể cả phần làm thử.

EN: Expected time: about 20 seconds per pair, that is, about 2 hours for each rater, including the practice part.

Note:
- Out of context, "khoảng 2 giờ" could mean "around 2 o'clock". Here "cho mỗi người" (for each person) makes the reading "about 2 hours" clear.
- "kể cả phần làm thử" (including the practice part) can attach to the 2-hour total only, or to the 20-seconds-per-pair rate as well. The more natural reading is the total.

---

## Terms rendered inconsistently across lines

- "đánh giá" is rendered "assess" in lines 1, 5 and 6 ("Không đánh giá được" = "Cannot assess"). In line 7, "người đánh giá" is rendered "rater" (literally "person who assesses"). The Vietnamese is the same verb throughout. The English varies only for idiom.
- "kém" is rendered "worse" for "kém hơn" in line 2 and "poor" for "kém như nhau" in line 5. The Vietnamese word is the same, but its strength differs: comparative in line 2, absolute in line 5 (see the notes).
- The lines that judge a caption use "tốt hơn" (better) in lines 1 and 3 and "kém hơn" (worse) in line 2. These are two poles, not an inconsistency, but the polarity is not symmetric: correctness is phrased as a penalty ("worse") and completeness as a reward ("better").
- Within the block, these are rendered the same way everywhere: "chú thích" (caption), "ảnh / bức ảnh" (picture), "xét" (consider), "chọn" (choose), "cặp" (pair), and the button labels "Ngang nhau" / "Không đánh giá được" (identical bytes in lines 5 and 6).
