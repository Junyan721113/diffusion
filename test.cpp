#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;

const double alpha = 0.5;
const double e = exp(1.0);
const double eh = exp(0.5);
const double w1 = (alpha / 4) * e / (e + eh);
const double w2 = (alpha / 4) * eh / (e + eh);

void onMouse(int event, int x, int y, int flags, void* param) {
    Mat pMat = *reinterpret_cast<Mat*>(param);
    switch (event)
    {
    case EVENT_LBUTTONDOWN:
        pMat.at<Vec3d>(y, x) = Vec3d(100000.0, 100000.0, 100000.0);
        break;
    default:
        break;
    }
}

int main() {
    Mat MStart = imread("Start.bmp"), Mdiff;
    MStart.convertTo(Mdiff, CV_64FC3);

    Mat kernel = (Mat_<double>(3, 3) << 
        w2, w1, w2,
        w1, (1.0 - alpha), w1,
        w2, w1, w2);
    
    imshow("diffusion", MStart);
    setMouseCallback("diffusion", onMouse, reinterpret_cast<void*>(&Mdiff));
    VideoWriter writer = VideoWriter("res.avi", VideoWriter::fourcc('X', 'V', 'I', 'D'), 30, MStart.size());
    int cnt = 0;
    while(waitKey(1) != 'q') {
        filter2D(Mdiff, Mdiff, -1, kernel);
        Mdiff.convertTo(MStart, CV_8UC3);
        imshow("diffusion", MStart);
        if(++cnt % 1 == 0) {
            cout << "Frame " << cnt << endl;
            writer << MStart;
        }
    }
    writer.release();
    return 0;
}
