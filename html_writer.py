
def write_html(results, filename):

    en='\r\n'   

    with open(filename, "w") as fout:
        fout.write('<!DOCTYPE html>'+en)
        fout.write('<html>'+en)
        fout.write('<body>'+en)
        
        fout.write("<h2>Top Events for Russell</h2>"+en)
        
        for el in results:
            fout.write("<center>"+en)
            fout.write("<a href=ticketmaster.com"+el+">View on ticketmaster!</a>"+en)
            fout.write("</center>"+en)
            fout.write("<br>"+en)
            fout.write("<br>"+en)
            fout.write("<br>"+en)
        fout.write("</body>"+en)
        fout.write("</html>"+en)
        
if __name__ == "__main__":
    sample = ("https://pbs.twimg.com/profile_images/657199367556866048/EBEIl2ol.jpg")
    write_html(sample)