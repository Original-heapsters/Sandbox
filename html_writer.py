
def write_html(results):

    en='\r\n'   

    with open("results.html", "w") as fout:
        fout.write('<!DOCTYPE html>'+en)
        fout.write('<html>'+en)
        fout.write('<body>'+en)
        
        for el in results:
            fout.write("<center>"+en)
            fout.write("<h2>"+el[0]+"</h2>"+en)
            fout.write("<img src="+el[1]+"/>"+en)
            fout.write("<br>"+en)
            fout.write("<a href=ticketmaster.com"+el[2]+">"+el[0]+"</a>"+en)
            fout.write("</center>"+en)
            fout.write("<br>"+en)
            fout.write("<br>"+en)
            fout.write("<br>"+en)
        fout.write("</body>"+en)
        fout.write("</html>"+en)
        
if __name__ == "__main__":
    sample = (("Adeles concert", "https://pbs.twimg.com/profile_images/657199367556866048/EBEIl2ol.jpg", "ticketmaster.com"),("Adeles concert", "https://pbs.twimg.com/profile_images/657199367556866048/EBEIl2ol.jpg", "ticketmaster.com"))
    write_html(sample)