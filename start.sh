
curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
sudo python3 install_gpu_driver.py

mkdir -p depth/depth_result
mkdir -p depth/depth_result_cut
wget https://github.com/Sxela/ArcaneGAN/releases/download/v0.4/ArcaneGANv0.4.jit
sudo apt install python3-pip
pip3 install --upgrade pip
pip3 install -r requirements.txt

