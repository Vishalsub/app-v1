python -m src.lerobot.async_inference.robot_client \
  --server_address=127.0.0.1:8080 \
  --robot.type=so101_follower \
  --robot.port=/dev/tty.usbmodem5AB01834431 \
  --robot.id=my_awesome_follower_arm_5 \
  --robot.cameras='{
      "wrist":   { "type": "opencv", "index_or_path": 0, "width": 1920, "height": 1080, "fps": 30 },
      "context": { "type": "opencv", "index_or_path": 1, "width": 1920, "height": 1080, "fps": 30 }
  }' \
  --policy_type=act \
  --pretrained_name_or_path=ceva-automation-sg/my_act-policy-50-new \
  --actions_per_chunk=100 \
  --chunk_size_threshold=0.5 \
  --policy_device=mps


  ------------------
lerobot-train \
  --dataset.repo_id=ceva-automation-sg/smolVLA_cali \
  --policy.type=act \
  --output_dir=outputs/train/ceva-log-act \
  --job_name=my_act_training \
  --policy.device=cuda \
  --policy.repo_id=\$HF_USER/my_act-policy-SL \
  --wandb.enable=true \

  python -m src.lerobot.async_inference.policy_server --host=127.0.0.1 --port=8080


  79a7863015151ad7c3ad9aff7c2d2479fbe4f137

  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


  
