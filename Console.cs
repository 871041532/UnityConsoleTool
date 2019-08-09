using UnityEngine;
using System.Runtime.InteropServices;
using System;
using System.IO;
using Microsoft.Win32.SafeHandles;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Collections.Generic;
using System.Diagnostics;
using static UnityEngine.Application;
using System.Threading;

public static class Console
{
    static bool is_OpenDebug = true;
    static string m_UDPServerURL = "127.0.0.1";
    static string m_UDPServerPort = "10000";

    static UdpClient m_UDPClient = null;
    static IPEndPoint m_EndPoint = null;
    static Process m_ChildProcess;
    static LogCallback m_LogCallback;
    static UnityEngine.LogType m_LastLogType;

    #region 外部接口
    public static void Init()
    {
        if (!is_OpenDebug)
        {
            return;
        }
        if (Application.platform == RuntimePlatform.WindowsPlayer || Application.platform == RuntimePlatform.WindowsEditor)
        {
            RunPythonConsole();
        }
        m_LogCallback = ( condition,  stackTrace,  type) => {
            if (m_LastLogType != type)
            {
                m_LastLogType = type;
                SendUDP("#" + (int)type);
            }
            SendUDP(condition);
            if (type != UnityEngine.LogType.Log)
            {
                SendUDP(stackTrace);
            }         
        };
        Application.logMessageReceived += m_LogCallback;
    }

    public static void OnDestroy()
    {
        if (!(m_UDPClient is null))
        {
            m_UDPClient.Close();
            m_UDPClient.Dispose();
            m_UDPClient = null;
        }
        if (!(m_ChildProcess is null))
        {
            try
            {
                m_ChildProcess.Kill();
            }
            catch (Exception)
            {
            }
            m_ChildProcess = null;
        }
        if (is_OpenDebug)
        {
            Application.logMessageReceived -= m_LogCallback;
        }
    }
    #endregion

    #region 内部实现
    static void RunPythonConsole()
    {
        string cmd = string.Format(Environment.CurrentDirectory + "/Tools/DebugTool.py");
        m_ChildProcess = new System.Diagnostics.Process();
        m_ChildProcess.StartInfo.FileName = cmd;
        m_ChildProcess.StartInfo.Arguments = m_UDPServerPort;
        m_ChildProcess.Start();
    }

    static void SendUDP(string sendString)
    {
        if (m_UDPClient is null)
        {
            IPAddress remoteIP = IPAddress.Parse(m_UDPServerURL); //假设发送给这个IP
            m_EndPoint = new IPEndPoint(remoteIP, Convert.ToInt32(m_UDPServerPort));//实例化一个远程端点 
            m_UDPClient = new UdpClient(10001);
            AsyncReceive();
        }
        byte[] sendData = Encoding.UTF8.GetBytes(sendString);
        m_UDPClient.Send(sendData, sendData.Length, m_EndPoint);//将数据发送到远程端点 
    }

    static async void AsyncReceive()
    {
        string strs = "";
        try
        {
            UdpReceiveResult result = await m_UDPClient.ReceiveAsync();
            strs = Encoding.UTF8.GetString(result.Buffer);
        }
        catch (Exception e)
        {
            if (!(e is SocketException))
            {
                return;
            }
        }
        AsyncReceive();
        if (!(string.IsNullOrEmpty(strs)))
        {
            PraseReceive(strs);
        }  
    }

    static void PraseReceive(string strs)
    {
        if (strs[0] == '#')
        {
            var strs_list = strs.Split(' ');
            Action<string[]> action = null;
            GMDict.TryGetValue(strs_list[0], out action);
            if (action is null)
            {
                UnityEngine.Debug.LogError("未定义的GM函数：" + strs_list[0]);
            }
            else
            {
                action(strs_list);
            }
        }
        else
        {
            UnityEngine.Debug.LogError("无法解析的GM指令：" + strs);
        }
    }
    #endregion

    #region GM命令
    static Dictionary<string, Action<string[]>> GMDict = new Dictionary<string, Action<string[]>>() {
        { "#CreateGameObject", CreateGameObject},
        { "#SwitchWindow", SwitchWindow},
    };
    
    static void CreateGameObject(string[] args)
    {
        string objName = "default";
        if (args.Length > 1)
        {
            objName = args[1];
        }
        var obj = new GameObject(objName);
        UnityEngine.Debug.Log("Create ok " + objName);
    }

    static void SwitchWindow(string[] args)
    {
        var win = GameManager.Instance.m_UIMgr.SwitchSingleWindow(args[1]);
    }
    #endregion
}