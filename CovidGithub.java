import java.net.URL;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.file.Files;
import java.nio.channels.Channels;
import java.nio.channels.FileChannel;
import java.nio.channels.ReadableByteChannel;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import java.util.Scanner;
import java.util.Map;
import java.util.HashMap;

public class CovidGithub{
	
	public static void downloadURL(String url, String outputpath) throws Exception{
		ReadableByteChannel readChannel = Channels.newChannel(new URL(url).openStream());
		FileOutputStream fileOS = new FileOutputStream(outputpath);
		FileChannel writeChannel = fileOS.getChannel();
		writeChannel.transferFrom(readChannel, 0, Long.MAX_VALUE);
	}
	
	public static String join(String path1, String path2) {
		File file1 = new File(path1);
		File file2 = new File(file1, path2);
		return file2.getPath();
	}
	
	
	public static void downloadAllData(String outputdirectory, Map<String, String> sources) throws Exception{
		
		for(String source : sources.keySet()){
			String outpath = join(outputdirectory, sources.get(source));
			downloadURL(source, outpath);
		}

	}
	
	public static void zipFiles(String outputDirectory, Map<String, String> sources) throws Exception{
		
		File f = new File(join(outputDirectory, "COVID_19_Data.zip"));
		ZipOutputStream out = new ZipOutputStream(new FileOutputStream(f));
		
		for(String source : sources.keySet()){
			ZipEntry e = new ZipEntry(join(outputDirectory, sources.get(source)));
			out.putNextEntry(e);
			
			File entryFile = new File(join(outputDirectory, sources.get(source)));
			out.write(Files.readAllBytes(entryFile.toPath()));
		}
		out.close();
	}
	
	public static HashMap<String, String> readSources(String configFile) throws Exception{
		File file = new File(configFile);
		Scanner scan = new Scanner(file);
		
		HashMap<String, String> sources = new HashMap<String, String>();

		while(scan.hasNext()){
			String[] row = scan.next().split(",");
			sources.put(row[0], row[1]);
		}scan.close();

		return sources;
	
	}

	
	public static void main(String[] args) throws Exception{
		String outputDirectory = args[0];
		String configFile = args[1];
		HashMap<String, String> sources = readSources(configFile);
		
		downloadAllData(outputDirectory, sources);
		zipFiles(outputDirectory, sources);

	}
	
}
