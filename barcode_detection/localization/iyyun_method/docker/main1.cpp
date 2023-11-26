#include <string>
#include <stdlib.h>
#include <iostream>
#include <cstdio>
#include <fstream>

#include "gallo/gallo.h"
#include "soros/soros.h"
#include "yun/yun.h"

// key
const char* keys = 
    "{h        help |                      | print help message                            }"
    "{file          | /file/dir/file_name  | test image file(.bmp .jpg .png)               }";

int main(int argc, char* argv[])
{
	cv::CommandLineParser cmd(argc, argv, keys);
    if (cmd.has("help") || !cmd.check())
    {
		cmd.printMessage();
		cmd.printErrors();
		return 0;
    }
	
	std::string fn = cmd.get<std::string>("file");
	
	iy::Gallo mGallo;
	iy::Soros mSoros;
	iy::Yun mYun;

	cv::Mat frame_gray;
	cv::Mat frame = cv::imread(fn.c_str());
	
	if(frame.data == NULL) {
		std::cerr << "error! read image" << std::endl;
		return -1;
	}

	cv::cvtColor(frame, frame_gray, CV_BGR2GRAY);

	cv::Rect g_rt = mGallo.process(frame_gray, 20);
	cv::rectangle(frame, g_rt, cvScalar(0, 255, 0), 2);

	cv::Rect s_rt = mSoros.process(frame_gray, 20);
	cv::rectangle(frame, s_rt, cvScalar(255,0,0), 2);

	std::vector<iy::YunCandidate> list_barcode = mYun.process(frame_gray);

	std::ofstream output_file("/workspace/output/boundings.txt");
	
	if (!list_barcode.empty())
	{

		if (!output_file.is_open()) {
  			std::cerr << "Failed to open file" << std::endl;
  			return -1;
		}
		
		for (std::vector<iy::YunCandidate>::iterator it = list_barcode.begin(); it < list_barcode.end(); it++)
		{
			if (it->isBarcode)
			{
				cv::Rect y_rt = it->roi;
				cv::rectangle(frame, y_rt, cvScalar(0, 255, 255), 2);

				output_file << y_rt.x << ", "
                 << y_rt.y << ", "
                 << y_rt.width << ", "
                 << y_rt.height << std::endl;

			}
		}

		list_barcode.clear();
	}

	output_file.close();

	cv::imwrite("/workspace/output/img.jpg", frame);

	return 0;
}