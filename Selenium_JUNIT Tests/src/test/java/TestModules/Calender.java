package TestModules;

import static org.junit.Assert.assertEquals;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class Calender {
	WebDriver driver;
	String username;
	String password;
	@Before
	public void startBrowser() {
		System.setProperty("webdriver.chrome.driver", "C:\\driver\\chromedriver.exe");
	    driver= new ChromeDriver();
		driver.get("http://instructortool.us-east-2.elasticbeanstalk.com/");
		driver.findElement(By.id("login-btn")).click();
		WebElement userid=driver.findElement(By.id("identifierId"));
		userid.sendKeys("#######");
		userid.sendKeys(Keys.ENTER);
		WebDriverWait wait = new WebDriverWait(driver,30);
		WebElement asurite = wait.until(ExpectedConditions.elementToBeClickable(By.name("username")));
		asurite.sendKeys("#######");
		WebElement pwd = wait.until(ExpectedConditions.elementToBeClickable((By.name("password"))));
		pwd.sendKeys("########");
		pwd.sendKeys(Keys.ENTER);
	}
	@Test
	public void TestCalenderPageLaunch() {
		WebDriverWait wait = new WebDriverWait(driver,30);
		WebElement ctn_btn = wait.until(ExpectedConditions.elementToBeClickable(By.className("ZFr60d")));
		Actions actions = new Actions(driver);
		actions.moveToElement(ctn_btn).click().perform();
	    WebElement token_input=wait.until(ExpectedConditions.elementToBeClickable(By.id("token-textbox")));
	    token_input.sendKeys("7236~yKpPpbQL0FRRPSp7kl7FYT2e2cPs9cibnQCnLKGlCEuvSU2XnIsjnYqrfeOg1uim");
	    driver.findElement(By.id("continue-btn")).click();
		WebElement view = wait.until(ExpectedConditions.elementToBeClickable(By.className("btn")));
		view.click();
		WebElement calender = wait.until(ExpectedConditions.elementToBeClickable(By.id("btn-cal")));
		calender.click();
	    
	}
	@Test
	public void CheckButtons() {
		
		
	}
	@Test
	public void CalenderEvents() {
	}
	@After
	public void tearDown() {
		driver.close();
	}
}
