borregas_ave() {
    poetry run python src/main.py \
        --map="borregas_ave" \
        --min_obs=10 --max_obs=20 \
        --num_adc=6 --num_scenario=30
}

san_mateo() {
    poetry run python src/main.py \
        --map="san_mateo" \
        --min_obs=10 --max_obs=20 \
        --num_adc=6 --num_scenario=30
}

sunnyvale_loop() {
    poetry run python src/main.py \
        --map="sunnyvale_loop" \
        --min_obs=20 --max_obs=30 \
        --num_adc=6 --num_scenario=30
}

san_francisco() {
    poetry run python src/main.py \
        --map="san_francisco" \
        --min_obs=20 --max_obs=30 \
        --num_adc=6 --num_scenario=30
}
