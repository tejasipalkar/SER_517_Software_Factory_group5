package TestModules;

import static org.junit.Assert.assertEquals;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Set;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Cookie;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.sun.java_cup.internal.runtime.Scanner;
public class Login {
	WebDriver driver;
	String username;
	String password;
	@Before
	public void startBrowser() {
		System.setProperty("webdriver.chrome.driver", "C:\\driver\\chromedriver.exe");
	    driver= new ChromeDriver();
	    driver.get("http://instructortool.us-east-2.elasticbeanstalk.com/");
	    
	}
	@Test
	public void TestGmail() throws IOException {
		
		
		driver.findElement(By.id("login-btn")).click();
		WebElement userid=driver.findElement(By.id("identifierId"));
		userid.sendKeys("#####");
		userid.sendKeys(Keys.ENTER);
		WebDriverWait wait = new WebDriverWait(driver,10);
		WebElement pwd = wait.until(ExpectedConditions.elementToBeClickable((By.name("password"))));
		pwd.sendKeys("#####");
		pwd.sendKeys(Keys.ENTER);
		Boolean result = wait.until(ExpectedConditions.textToBe(By.tagName("body"), "Please login via asu.edu account"));
		assertEquals("Login with non-asu id tested successfully",true, result);
			
		
}
	
	@Test
	public void ASULogin() throws IOException, InterruptedException{
		driver.get("http://instructortool.us-east-2.elasticbeanstalk.com/");
		driver.findElement(By.id("login-btn")).click();
		WebElement userid=driver.findElement(By.id("identifierId"));
		userid.sendKeys("#####");
		userid.sendKeys(Keys.ENTER);
		WebDriverWait wait = new WebDriverWait(driver,10);
		WebElement asurite = wait.until(ExpectedConditions.elementToBeClickable(By.name("username")));
		asurite.sendKeys("#####");
		WebElement pwd = wait.until(ExpectedConditions.elementToBeClickable((By.name("password"))));
		pwd.sendKeys("#######");
		pwd.sendKeys(Keys.ENTER);
		driver.wait(10);	
		WebElement ctn_btn = wait.until(ExpectedConditions.elementToBeClickable(By.className("ZFr60d")));
		Actions actions = new Actions(driver);
		actions.moveToElement(ctn_btn).click().perform();
		String currentURL = driver.getCurrentUrl();
		Boolean result= currentURL.contains(currentURL);
		assertEquals(true, result);	
	}
	
	@After
	public void tearDown() {
		driver.close();
	}
}
