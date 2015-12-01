#!/usr/bin/php
<?php
require_once ('ZeusSpider/ZeusSpider.php');
require_once ('../util/phpmail.php');
class backupCheck extends ZeusSpider {
    function __construct() {
        parent::__construct ();
    }
    
    private $exts = array(".zip",".tar",".sql",".rar",".gz",".tgz",".tar.gz",".7z",".bz2",".tar.bz2",".bzip",".bak");
    private $files = array("server","tmp","inc","lib","wwwroot","www","web","db","wangzhan","old","back","cart","data");

    function scan($url){
        $this->curl->add(
                         array(
                               'url'=> $url,
                               'args' => array (
                                                'url' => $url
                                                ) 

                               ),
                         function($r,$args){

                             if($r['info']['http_code'] == 200 &&  $r['info']['size_download'] > 3524051){
                                 var_dump($args,$r['info']['size_download']);
                                 echo "~~wakaka";
                             }
                         }
        );
    }       

    function scanDomain($target, $port){
        //todo task check

        foreach($this->exts as $ext){
            foreach($this->files as $file){                                
                if ($port == 443){
                    $protocal = "https";
                }else{
                    $protocal = "http";
                }
                $url =  $protocal."://".$target.':'.$port.'/'.$file.$ext;
                //echo $url.PHP_EOL;
                $this->scan($url);                
            }
            
        }
        //todo 
    }
    

    /**
     * 备份文件扫描开始
     */
    function start($domain,$port) {
        //$domain = "127.0.0.1";
        //$port = "80";
        /*
        $this->curl->cbInfo = array (
                                     $this,
                                     'cbCurlInfo' 
                                     );        
        */
        
        $this->scanDomain($domain,$port);
        $this->curl->start();        
    }


    /**
     * 写数据库
     *
     * @see ZeusSpider::data()
     */
    function data(array $args) {
        if (isset ( $args ['type'] )) {
            $type = $args ['type'];
        } else {
            $type = 'insert';
        }
        if ($type == 'insert') {
            $this->db->insert ( $args ['table'], $args ['row'], 'ignore' );
            return $this->db->lastInsertId ();
        } else {
            return $this->db->update ( $args ['table'], $args ['row'], 'id=' . $args ['id'] );
        }
    }
}


$opts = getopt("t:p:");
$domain = $opts['t'];
$port = $opts['p'];

if($domain && $port){
    $backupCheck = new backupCheck ();
    $backupCheck->start ($domain, $port);
}else{
    echo "Usage: backup_check.php -t 127.0.0.1 -p 80";
}

