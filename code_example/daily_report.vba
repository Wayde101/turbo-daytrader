Sub new_report()
    '¨å»©£ÃÄ»ÃÍoffset Å¢.

    Dim dod_col As Integer
    Dim wow_col As Integer
    Dim cur_col As Integer
    Dim tc As Integer
    Dim result As String
    Dim strFile As String
    
    strFile = "d:\report\daily-report.html"
    
    Open strFile For Output As #1
    
    'ñ¡ÜÐý,«ä£ÃÄ offset ýµ.
    Const jiuv_offset = 5
    Const xinv_offset = 14
    Const quanbu_offset = 42 - 1

    tc = Me.UsedRange.Columns.Count
    
    '£Ãcol íÈÆã.
    wow_col = tc - 4
    dod_col = tc - 5
    cur_col = tc - 6
        

    result = "<!DOCTYPE html PUBLIC ""-//W3C//DTD XHTML 1.0 Transitional//EN"" ""http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd""" & vbCrLf
    result = result & "<html xmlns=""http://www.w3.org/1999/xhtml"">" & vbCrLf
    result = result & "<head>" & vbCrLf
    result = result & "<meta http-equiv=""Content-Type"" content=""text/html; charset=gbk"" />" & vbCrLf
    result = result & "<title> Õ¨Ü¨µ³ </title>" & vbCrLf
    result = result & "</head><body id=""body"" >"
    
    gn_b = "<font size=""9pt"" style=""font-size: 9pt; font-family: &quot;Arial&quot;,&quot;sans-serif&quot;;"" >"
    gn_e = "</font>"
    bm_b = "<span style=""font-size: 9pt; color: black;font-weight:700;"">"
    bm_e = "</span>"
    
    result = result & gn_b
    result = result & "<br>" & vbCrLf & bm_b & "Ñ÷Øü¸ê ¨Âæsearch+list©º" & bm_e
    result = result & "<br>" & vbCrLf
    
    
    result = result & "<br>" & vbCrLf
    result = result & "CTRºÂæÑ÷ª" & cell_out("p", 208, cur_col) & "," & cell_out("p", 208, wow_col)
    result = result & " search " & cell_out("p", 201, cur_col) & "," & cell_out("p", 201, wow_col) & "; "
    result = result & "TO B " & cell_out("p", 206, cur_col) & "," & cell_out("p", 206, wow_col) & "¢TO C " & cell_out("p", 207, cur_col) & "," & cell_out("p", 207, wow_col) & ")" & "£"
    

    result = result & "<br>" & vbCrLf
    result = result & "search pvº" & cell_out("m", 49, cur_col) & "," & cell_out("p", 49, wow_col) & " £"


    result = result & "<br>" & vbCrLf
    result = result & "UVº" & cell_out("m", 80, cur_col) & "," & cell_out("p", 80, wow_col)
    result = result & " (search " & cell_out("p", 77, wow_col) & "; list " & cell_out("p", 74, wow_col) & ");"
    result = result & "«øc2cª " & cell_out("m", 83, cur_col) & "," & cell_out("p", 83, wow_col) & " £"
    
    
    result = result & "<br>" & vbCrLf
    result = result & bm_b & "ÃÊ-É»UVª¯Êº" & bm_e & "Ñ÷ª " & cell_out("p", 101, cur_col) & "," & cell_out("p", 101, wow_col)
    result = result & " (search " & cell_out("p", 98, wow_col) & "; list " & cell_out("p", 95, wow_col) & ");"
    result = result & "«øc2cª " & cell_out("p", 105, cur_col) & "," & cell_out("p", 105, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf
    result = result & "ÃÊ-ã÷UVª¯ÊºÑ÷ª " & cell_out("p", 102, cur_col) & "," & cell_out("p", 102, wow_col)
    result = result & " (search " & cell_out("p", 99, wow_col) & "; list " & cell_out("p", 96, wow_col) & ");"
    result = result & "«øc2cª " & cell_out("p", 104, cur_col) & "," & cell_out("p", 104, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf
    result = result & "ã÷-É»UVª¯ÊºÑ÷ª " & cell_out("p", 103, cur_col) & "," & cell_out("p", 103, wow_col)
    result = result & " (search " & cell_out("p", 100, wow_col) & "; list " & cell_out("p", 97, wow_col) & ");"
    result = result & "«øc2cª " & cell_out("p", 106, cur_col) & "," & cell_out("p", 106, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf
    result = result & "PVÛµº" & cell_out("n", 244, cur_col) & "ª" & "," & cell_out("p", 244, wow_col)
    result = result & " (search " & cell_out("p", 243, wow_col) & ", list " & cell_out("p", 242, wow_col) & ";TO B " & cell_out("p", 241, wow_col) & ",TO C " & cell_out("p", 238, wow_col) & ")" & ""
    result = result & "«øc2cª " & cell_out("n", 254, cur_col) & "," & cell_out("p", 254, wow_col) & " £"

    result = result & "<br>" & vbCrLf
    result = result & "IPVÛµº" & cell_out("n", 275, cur_col) & "ª" & "," & cell_out("p", 275, wow_col)
    result = result & " (search " & cell_out("p", 274, wow_col) & ", list " & cell_out("p", 273, wow_col) & ";TO B " & cell_out("p", 272, wow_col) & ",TO C " & cell_out("p", 269, wow_col) & ")" & "£"
    result = result & "«øc2cª " & cell_out("n", 285, cur_col) & "," & cell_out("p", 285, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf
    result = result & "UVÛµ " & cell_out("n", 222, cur_col) & "ª," & cell_out("p", 222, wow_col)
    result = result & " (search " & cell_out("p", 221, wow_col) & "; list " & cell_out("p", 220, wow_col) & ")£"
    result = result & "«øc2cª " & cell_out("n", 223, cur_col) & "," & cell_out("p", 223, wow_col) & " £"

    result = result & "<br>" & vbCrLf
    result = result & "á±UVÛµ " & cell_out("n", 1046, cur_col) & "," & cell_out("p", 1046, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf
    result = result & "á±ÃÊ-É»UVª¯Êº" & cell_out("p", 1047, cur_col) & "," & cell_out("p", 1047, wow_col) & " £"
 

    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "Üåéö¨ÂæÑ÷+ÉæÑ÷©º"
    result = result & "<br>" & vbCrLf
    result = result & "IPVºÑ÷ª" & cell_out("m", 31, cur_col) & "," & cell_out("p", 31, wow_col)
    result = result & " (search " & cell_out("p", 30, wow_col) & "; list " & cell_out("p", 29, wow_col) & ");"
    result = result & "«øc2cª " & cell_out("m", 32, cur_col) & "," & cell_out("p", 32, wow_col) & ";(TO B " & cell_out("m", 28, cur_col) & "," & cell_out("p", 28, wow_col) & "¢TO C " & cell_out("m", 25, cur_col) & "," & cell_out("p", 25, wow_col) & ")" & "£"
    
    
    result = result & "<br>" & vbCrLf
    result = result & "CTRºÑ÷ª" & cell_out("p", 213, cur_col) & "," & cell_out("p", 213, wow_col)
    result = result & " (search " & cell_out("p", 210, cur_col) & "," & cell_out("p", 210, wow_col) & "; list " & cell_out("p", 209, cur_col) & "," & cell_out("p", 209, wow_col) & ";"
    result = result & "TO B " & cell_out("p", 211, cur_col) & "," & cell_out("p", 211, wow_col) & "¢TO C " & cell_out("p", 212, cur_col) & "," & cell_out("p", 212, wow_col) & ")" & "£"
    
    result = result & "<br>" & vbCrLf
    result = result & "PVºÑ÷ª" & cell_out("m", 52, cur_col) & "," & cell_out("p", 52, wow_col)
    result = result & " (search " & cell_out("p", 51, wow_col) & "; list " & cell_out("p", 50, wow_col) & ");"
    result = result & "«øc2cª " & cell_out("m", 53, cur_col) & "," & cell_out("p", 53, wow_col) & " £"

    
    result = result & "<br>" & vbCrLf
    result = result & "§¶¦É»îº Ñ÷ý¼ª " & cell_out("wy", 178, cur_col) & "," & cell_out("p", 178, wow_col) & " "
    result = result & "(search " & cell_out("p", 177, wow_col) & ",list " & cell_out("p", 176, wow_col) & ");" & " TO B " & cell_out("wy", 175, cur_col) & "," & cell_out("p", 175, wow_col) & "¢TO C " & cell_out("wy", 172, cur_col) & "," & cell_out("p", 172, wow_col) & "»"
    result = result & "«øc2cª " & cell_out("yy", 179, cur_col) & ", " & cell_out("p", 179, wow_col) & "£"
    
    
    result = result & "<br>" & vbCrLf
    result = result & "íÚ¶§¶¦É»îº Ñ÷ý¼ª " & cell_out("y", 1070, cur_col) & "," & cell_out("p", 1070, wow_col) & " "
    result = result & "(search " & cell_out("y", 1069, cur_col) & "," & cell_out("p", 1069, wow_col) & ";list " & cell_out("y", 1068, cur_col) & "," & cell_out("p", 1068, wow_col) & ")£"
    
    
    result = result & "<br>" & vbCrLf
    result = result & "IPVÛµº" & cell_out("n", 284, cur_col) & "ª" & "," & cell_out("p", 284, wow_col)
    result = result & " (search " & cell_out("p", 283, wow_col) & ", list " & cell_out("p", 282, wow_col) & ";TO B " & cell_out("p", 281, wow_col) & ",TO C " & cell_out("p", 278, wow_col) & ")" & "£"
    
    result = result & "<br>" & vbCrLf
    result = result & "PVÛµº" & cell_out("n", 253, cur_col) & "ª" & "," & cell_out("p", 253, wow_col)
    result = result & " (search " & cell_out("p", 252, wow_col) & ", list " & cell_out("p", 251, wow_col) & ";TO B " & cell_out("p", 250, wow_col) & ",TO C " & cell_out("p", 247, wow_col) & ")" & "£"
    
    result = result & "<br>" & vbCrLf
    result = result & " Search÷¸ê¼Èº¼«øpvÈý " & cell_out("p", 1075, cur_col) & "," & cell_out("p", 1075, wow_col) & ";"
    result = result & " ¼«øuvÈý " & cell_out("p", 1076, cur_col) & "," & cell_out("p", 1076, wow_col) & ";"
    result = result & " ¼«øipvÈý " & cell_out("p", 1077, cur_col) & "," & cell_out("p", 1077, wow_col) & ";"
    result = result & " ¼«ø§¶¦É»Èý " & cell_out("p", 1078, cur_col) & "," & cell_out("p", 1078, wow_col) & "£"

    
    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf
    result = result & "êÌÑ÷:PVª" & cell_out("m", 463, cur_col) & "," & cell_out("p", 463, wow_col) & " ,UVª" & cell_out("wy", 464, cur_col) & "," & cell_out("p", 464, wow_col) & ";"
    result = result & "§¶¦ÏÚ¶É»îª" & cell_out("wy", 468, cur_col) & "," & cell_out("p", 468, wow_col) & ";"
    result = result & "UVÛµª" & cell_out("n", 472, cur_col) & "," & cell_out("p", 472, wow_col) & "£"
    
    
    'result = result & "<br>" & vbCrLf
    'result = result & "´¼ºPVª" & cell_out("n", 436, cur_col) & "," & cell_out("p", 436, wow_col) & " ,UVª" & cell_out("n", 437, cur_col) & "," & cell_out("p", 464, wow_col) & ";"
    'result = result & "§¶¦É»îª" & cell_out("n", 442, cur_col) & "Ê," & cell_out("n", 441, cur_col) & "ª;"
    'result = result & "UVÛµª" & cell_out("n", 443, cur_col) & "," & cell_out("p", 443, wow_col) & "£"
    
    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "B2Cº"
    result = result & "<br>" & vbCrLf
    result = result & "¹¯é¨search©ºã÷/¹ÖPV ª" & cell_out("p", 1038, cur_col) & "," & cell_out("p", 1038, wow_col) & ";" & "²ÇÊª" & cell_out("p", 1037, cur_col) & "," & cell_out("p", 1037, wow_col) & "£"
    result = result & "<br>" & vbCrLf
    result = result & "¹¯é¨list©ºã÷/¹ÖPV ª" & cell_out("p", 1036, cur_col) & "," & cell_out("p", 1036, wow_col) & ";" & "²ÇÊª" & cell_out("p", 1035, cur_col) & "," & cell_out("p", 1035, wow_col) & "£"
    result = result & "<br>" & vbCrLf
    result = result & "¹¯é¨list+search©ºã÷/¹ÖPV ª" & cell_out("p", 1042, cur_col) & "," & cell_out("p", 1042, wow_col) & ";" & "²ÇÊª" & cell_out("p", 1040, cur_col) & "," & cell_out("p", 1040, wow_col) & "£"

    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "ÌÇÑ÷º"
    result = result & "<br>" & vbCrLf
    result = result & "IPVºÑ÷ª" & cell_out("m", 343, cur_col) & "," & cell_out("p", 343, wow_col)
    result = result & " (search " & cell_out("p", 342, wow_col) & "; list " & cell_out("p", 341, wow_col) & ");"
    result = result & "ÌÇIPVª " & cell_out("m", 344, cur_col) & "," & cell_out("p", 344, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf
    result = result & "CTRºÑ÷ª" & cell_out("p", 404, cur_col) & "," & cell_out("p", 404, wow_col)
    result = result & " (search " & cell_out("p", 403, wow_col) & "; list " & cell_out("p", 402, wow_col) & ")£"
    
    result = result & "<br>" & vbCrLf
    result = result & "UVºlistª" & cell_out("m", 361, cur_col) & "," & cell_out("p", 361, wow_col) & "¬" & "searchª" & cell_out("m", 364, cur_col) & "," & cell_out("p", 364, wow_col) & "»"
    result = result & "«øb2cª " & cell_out("m", 367, cur_col) & "," & cell_out("p", 367, wow_col) & " £"
    
    result = result & "<br>" & vbCrLf & "ÃÊ-É»UVª¯Êº"
    result = result & "listª" & cell_out("p", 371, cur_col) & "," & cell_out("p", 371, wow_col) & ";" & "searchª" & cell_out("p", 374, cur_col) & "," & cell_out("p", 374, wow_col) & ";" & "«øb2cª" & cell_out("p", 377, cur_col) & "," & cell_out("p", 377, wow_col) & "£"
    
    result = result & "<br>" & vbCrLf
    result = result & "§¶¦É»îº Ñ÷ý¼ª " & cell_out("wy", 394, cur_col) & "," & cell_out("p", 394, wow_col)
    result = result & "(search " & cell_out("p", 393, wow_col) & ",list " & cell_out("p", 392, wow_col) & ");"
    result = result & "«øb2cª " & cell_out("wy", 395, cur_col) & ", " & cell_out("p", 395, wow_col) & "£"
    
    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "¬êºº"
    result = result & "<br>" & vbCrLf
    result = result & "PVº" & cell_out("m", 1053, cur_col) & "," & cell_out("p", 1053, wow_col) & " ,"
    result = result & "UVº " & cell_out("m", 1054, cur_col) & "," & cell_out("p", 1054, wow_col) & " ,"
    result = result & "íÚ¶É»º " & cell_out("m", 1055, cur_col) & "," & cell_out("p", 1055, wow_col) & " ,"

    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "ÅÐñº"
    result = result & "<br>" & vbCrLf
    result = result & "PVº" & cell_out("m", 1060, cur_col) & "," & cell_out("p", 1060, wow_col) & " ;"
    result = result & "UVº " & cell_out("m", 1061, cur_col) & "," & cell_out("p", 1061, wow_col) & " £"
       
    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "ÞáûÊ¨Â+É©º" & cell_out("p", 489, cur_col) & "," & cell_out("p", 489, wow_col) & "£"
    result = result & "<br>" & vbCrLf & "ÚßÌ·ýº" & cell_out("y", 451, cur_col) & "," & cell_out("p", 451, wow_col) & "£"

    result = result & "<br>" & vbCrLf
    result = result & "<br>" & vbCrLf & "ûåpvº" & cell_out("m", 1086, cur_col) & "," & cell_out("p", 1086, wow_col) & " ;"
    result = result & "ÌµÑ÷pvº" & cell_out("m", 1083, cur_col) & "," & cell_out("p", 1083, wow_col) & " ;"
    result = result & "ÔÍÑ÷pvº" & cell_out("m", 1084, cur_col) & "," & cell_out("p", 1084, wow_col) & "£" & vbCrLf
    
    ' body_end_here_dont_remove_it
    result = result & gn_e & "</body>" & vbCrLf
    

    Debug.Print result
    
    Print #1, result
    Close #1
    
    'MsgBox result

    
    
End Sub

Function cell_out(ByVal fmt As String, ByVal rol As Integer, ByVal col As Integer) As String
    tcn = Me.UsedRange.Columns.Count
    
    red_b = "<span style=""font-size: 9pt; font-family: &quot;Arial&quot;,&quot;sans-serif&quot;; color: red;"">"
    green_b = "<span style=""font-size: 9pt; font-family: &quot;Arial&quot;,&quot;sans-serif&quot;; color: green;"">"
    endmark = "</span>"
    
    If col = tcn - 4 And Cells(rol, col) > 0 Then
        Prefix = red_b & "+"
    End If
    
    If col = tcn - 4 And Cells(rol, col) < 0 Then
        Prefix = green_b
    End If
    
    If fmt = "p" Then
        cell_out = Prefix & Format(Cells(rol, col).Value, "percent")
    ElseIf fmt = "n" Then
        cell_out = Prefix & Format(Cells(rol, col).Value, "standard")
    ElseIf fmt = "m" Then
        cell_out = Prefix & Format(Cells(rol, col).Value / 1000000, "fixed") & "M"
    ElseIf fmt = "wy" Then
        cell_out = Prefix & Format(Cells(rol, col).Value / 10000, "fixed") & "òª"
    ElseIf fmt = "yy" Then
        cell_out = Prefix & Format(Cells(rol, col).Value / 100000000, "fixed") & "Úª"
    ElseIf fmt = "y" Then
        cell_out = Prefix & Format(Cells(rol, col).Value / 100000000, "fixed") & "Ú"
        
    End If
    
     
    If Cells(rol, tcn) = "30ìîÍã" Then
        endstr = "ü"
    ElseIf Cells(rol, tcn - 1) = "30ìîßã" Then
        endstr = "ï"
    End If
    
    
    cell_out = cell_out & endstr & endmark
End Function

