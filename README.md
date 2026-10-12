# Si AI agent — Executor starter

শর্ট ডিস্ক্রিপশন: Si AI agent হল একটি লোকাল, অনুমোদন-ভিত্তিক (Approve→Execute) AI Executor স্টার্টার কিট। এটি একটি নিরাপদ, whitelist-ভিত্তিক এক্সিকিউটর সার্ভিস দিয়ে আসে যা আপনি লোকাল চ্যাট (যেমন GPT4All WebUI) থেকে প্রস্তাব পাঠিয়ে ব্যবহার করতে পারবেন।

এই রিপোজিটরিতে যা আছে:
- app.py — Flask ভিত্তিক Executor সার্ভিস (propose, list, approve endpoints)
- whitelist.json — অনুমোদিত (allowed) কমান্ডের তালিকা (absolute path + description)
- scripts/ — উদাহরণ স্ক্রিপ্ট (backup, cleanup)
- Dockerfile — non-root executor ইমেজ তৈরির জন্য
- docker-compose.yml — দ্রুত ডেভ/রান কনফিগ
- propose-send.js — ছোট JS উদাহরণ যাতে আপনি Chat UI থেকে প্রস্তাব পাঠাতে পারেন
- requirements.txt — Python package list

নির্দেশনা (Quickstart)

1) রেপো ক্লোন করুন

    git clone https://github.com/mdrahamatalimolla/ai-executor-starter.git
    cd ai-executor-starter

2) স্ক্রিপ্টগুলো executable করুন

    sudo mkdir -p /opt/executor
    sudo chown $USER:$USER /opt/executor
    cp -r scripts /opt/executor/
    chmod +x /opt/executor/scripts/*.sh

3) Docker ব্যবহার করে চালান (সরলভাবে)

    # বিল্ড ইমেজ
    sudo docker compose build

    # চালান (port 5000 লোকাল হোস্টে exposed)
    sudo docker compose up -d

4) প্রস্তাব পাঠানো (উদাহরণ curl)

    curl -X POST -H "Content-Type: application/json" \
      -d '{"command":"cleanup_tmp","args":["/tmp/testdir"],"note":"clean old tmp"}' \
      http://127.0.0.1:5000/propose

5) প্রস্তাব তালিকা দেখুন

    curl http://127.0.0.1:5000/proposals

6) Approve ও Execute (API_KEY প্রয়োজন — ডকার কম্পোজে environment এ সেট করা আছে)

    curl -X POST -H "Content-Type: application/json" -H "X-API-KEY: REPLACE_WITH_STRONG_KEY" \
      -d '{"approve": true}' \
      http://127.0.0.1:5000/approve/1

নোটস:
- এই প্রকল্পটি একটি স্টার্টার কিট; আপনার পরিবেশ অনুযায়ী whitelist.json ও scripts কাস্টমাইজ করুন।
- নিরাপত্তার জন্য executor সার্ভিস শুধুমাত্র লোকাল নেটওর্কে চালান বা SSH/VPN ব্যবহার করুন।
- বড় মডেল বা WebUI (GPT4All) আলাদাভাবে চালাতে হবে — README তে লিংক দেয়া আছে।

হেল্প লাগলে ইস্যু খুলুন বা আমাকে বলুন।
