<?php
abstract class ZeusSpider {
	private $lastUpdate = 0;
	protected $curl;
	function __construct() {
		if (time () - $this->lastUpdate > 864000) {
			$this->sdkUpdate ( 'CurlMulti' );
		}
		require_once (__DIR__ . '/CurlMulti.php');
		require_once (__DIR__ . '/phpQuery.php');
		$this->curl = new CurlMulti ();
		// 设置最大并发数
		$this->curl->maxTrhead = 10;
		// 默认错误回调
		$this->curl->cbFail = array (
				$this,
				'cbCurlFail' 
		);
		// 默认信息回调
		$this->curl->cbInfo = array (
				$this,
				'cbCurlInfo' 
		);
	}
	
	/**
	 * 每个目录最多4096个文件(可以保持很好的IO性能),4096^2=16777216,4096^3=68719476736
	 *
	 * @param string $key        	
	 * @param number $level        	
	 * @return string 文件相对路径
	 */
	function hashPath($key, $level = 2) {
		$file = md5 ( $key );
		if ($level == 2) {
			$file = substr ( $file, 0, 3 ) . '/' . substr ( $file, 3 );
		} elseif ($level == 3) {
			substr ( $file, 0, 3 ) . '/' . substr ( $file, 3, 6 ) . '/' . substr ( $file, 6 );
		} else {
			throw new ErrorException ( 'Too many levels' );
		}
		return $file;
	}
	
	/**
	 * 返回开始和结束字符串之间的字符串
	 *
	 * @param string $str        	
	 * @param string $start
	 *        	开始字符串
	 * @param string $end
	 *        	结束字符串
	 * @param String $mode
	 *        	g 贪婪模式
	 *        	ng 非贪婪模式
	 */
	function subStr($str, $start, $end, $mode = 'g') {
		if (isset ( $start )) {
			$pos1 = strpos ( $str, $start );
		} else {
			$pos1 = 0;
		}
		if (isset ( $end )) {
			if ($mode == 'g') {
				$pos2 = strrpos ( $str, $end );
			} elseif ($mode == 'ng') {
				$pos2 = strpos ( $str, $end, $pos1 );
			} else {
				throw new ErrorException ( 'mode is invalid, mode=' . $mode );
			}
		} else {
			$pos2 = strlen ( $str );
		}
		if (false === $pos1 || false === $pos2 || $pos2 < $pos1) {
			return false;
		}
		$len = strlen ( $start );
		return substr ( $str, $pos1 + $len, $pos2 - $pos1 - $len );
	}
	
	/**
	 * 默认CurlMulti错误回调
	 *
	 * @param array $error        	
	 */
	function cbCurlFail($error, $args) {
		$err = $error ['error'];
		echo "\ncurl error, $err[0] : $err[1] ".json_encode($args)."\n";
	}
	
	/**
	 * 默认CurlMulti的信息回调
	 *
	 * @param array $info
	 *        	array('all'=>array(),'runnint'=>array())
	 * @throws \ErrorException
	 */
	function cbCurlInfo($info) {
		$all = $info ['all'];
		$cacheNum = $all ['cacheNum'];
		$taskPoolNum = $all ['taskPoolNum'];
		$finishNum = $all ['finishNum'];
		$taskFail = $all ['taskFailNum'];
		$speed = round ( $all ['downloadSpeed'] / 1024 ) . 'KB/s';
		$size = round ( $all ['downloadSize'] / 1024 / 1024 ) . "MB";
		$str = "\r";
		$str .= sprintf ( "speed:%-10s", $speed );
		$str .= sprintf ( 'download:%-10s', $size );
		$str .= sprintf ( 'cache:%-10dfinish:%-10d', $cacheNum, $finishNum );
		$str .= sprintf ( 'taskPoolNum:%-10d', $taskPoolNum );
		foreach ( $all ['taskRunningNumType'] as $k => $v ) {
			$str .= sprintf ( 'taskRunning' . $k . ':%-10d', $all ['taskRunningNumType'] [$k] );
		}
		$str .= sprintf ( 'taskRunningNoType:%-10d', $all ['taskRunningNumNoType'] );
		echo $str;
	}
	
	/**
	 * 处理http头不是200的请求
	 *
	 * @param unknown $info        	
	 * @return boolean
	 */
	function httpError($info) {
		if ($info ['http_code'] != 200) {
			$this->curl->error ( 'http error, code=' . $info ['http_code'] . ', url=' . $info ['url'] );
			return false;
		}
		return true;
	}
	
	/**
	 * html转码
	 *
	 * @param string $html        	
	 * @param string $in        	
	 * @param string $out        	
	 * @param string $content        	
	 */
	function charsetTrans($html, $in, $out = 'UTF-8') {
		$html = iconv ( $in, $out . '//IGNORE', $html );
		return preg_replace ( '/(<meta\s+.+?content=".+?charset=)(.+?)("\/?>)/i', "\\1$out\\3", $html, 1 );
	}
	
	/**
	 * 把html中的所有相对地址换成绝对地址
	 *
	 * @param string $html        	
	 * @param string $url        	
	 * @return string string
	 */
	function urlFull($html, $url) {
		$parseUrl = parse_url ( $url );
		$uri = str_replace ( '\\', '/', dirname ( $parseUrl ['path'] ) );
		return preg_replace_callback ( '/(\s+(src|href)=("|\')?)(?!http:\/\/)([^\\3]+?)\\3/i', array($this,'_cbUrlFull'), $html );
	}
	final function _cbUrlFull($match, $uri) {
		if (0 !== strpos ( $match [4], '/' )) {
			$match [4] = $uri . '/' . $match [4];
		}
		return $match [1] . $this->site->url . $match [4] . $match [3];
	}
	
	/**
	 * 返回CurlMulti对象
	 *
	 * @return CurlMulti
	 */
	function getCurlMulti() {
		return $this->curl;
	}
	
	/**
	 * 更新Sdk
	 *
	 * @param string $type
	 *        	null 更新ZeusSpider.php和CurlMulti.php
	 *        	CurlMulti 只更新CurlMulti.php
	 * @throws ErrorException
	 * @return boolean
	 */
	function sdkUpdate($type = null) {
        return true;
		$code = $this->getUpdateContent ( $type );
		$files = '';
		foreach ( $code as $k => $v ) {
			$file = __DIR__ . "/../$k";
			$dir = dirname ( $file );
			if (! is_dir ( $dir )) {
				mkdir ( $dir, 0755, true );
			}
			if (false === file_put_contents ( $file, $v )) {
				throw new ErrorException ( 'Failed to write ' . $k . '.php' );
			}
			$files = $k . "\n";
		}
		if (! isset ( $type )) {
			echo "\n=================================================\n";
			echo "Sdk updated sucessfully, please restart your app!\n";
			echo "updated files:\n";
			echo $files;
			echo "=================================================\n";
		}
		return true;
	}
	
	/**
	 * 获取更新内容
	 *
	 * @param string $type        	
	 * @return array
	 */
	private function getUpdateContent($type) {
		return true;
		$url = 'http://zeusspider.com/index/update';
		if (version_compare ( PHP_VERSION, '5.3.0' ) < 0) {
			$url .= '/52';
		} elseif (version_compare ( PHP_VERSION, '5.4.0' ) < 0) {
			$url .= '/53';
		} elseif (version_compare ( PHP_VERSION, '5.5.0' ) < 0) {
			$url .= '/54';
		}
		if (isset ( $type )) {
			$url .= '/' . $type;
		}
		$ch = curl_init ();
		$opt [CURLOPT_URL] = $url;
		$opt [CURLOPT_HEADER] = false;
		$opt [CURLOPT_CONNECTTIMEOUT] = 10;
		$opt [CURLOPT_TIMEOUT] = 30;
		$opt [CURLOPT_AUTOREFERER] = true;
		$opt [CURLOPT_USERAGENT] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11';
		$opt [CURLOPT_RETURNTRANSFER] = true;
		$opt [CURLOPT_FOLLOWLOCATION] = true;
		$opt [CURLOPT_MAXREDIRS] = 10;
		curl_setopt_array ( $ch, $opt );
		$r = curl_exec ( $ch );
		if (false === $r) {
			$errno = curl_errno ( $ch );
			$err = curl_error ( $ch );
			curl_close ( $ch );
			throw new ErrorException ( 'Update failed, ' . $errno . ' : error=' . $err );
		}
		curl_close ( $ch );
		$r = gzuncompress ( $r );
		$r = unserialize ( $r );
		if ($r ['errorCode'] != 0) {
			throw new ErrorException ( 'Update failed, error=' . $r ['errorMsg'] );
		}
		if ($type == 'CurlMulti') {
			$r ['code'] ['Sdk/ZeusSpider.php'] = preg_replace ( '/private \$lastUpdate\s*?=\s*?\d+?;(\r|\n)/', 'private $lastUpdate = ' . time () . ";\n", file_get_contents ( __FILE__ ), 1 );
		}
		return $r ['code'];
	}
}
