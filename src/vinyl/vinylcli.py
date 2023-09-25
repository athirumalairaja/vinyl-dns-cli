#!/usr/bin/python python

import argparse
import sys
import json
from .get_zone_info import get_zone_info
# from .get_record_set_info import get_record_set_info
from .search_record_set_info import search_record_set_info
from .create_record_set import create_record_set
from .delete_record_set import delete_record_set
from .update_record_set import update_record_set
from .create_alias import create_alias
from .search_alias import search_alias
from ip_control.ip_control_login import login
from ip_control.get_device_info import get_device
from ip_control.create_device import create_device
from ip_control.update_device import update_device
from ip_control.delete_device import delete_device
from .format_response import format_response, alias_response

record_set_name = None
ip_address = None
record_set_id = None
zone_id = None

def search_record(args):
    response = search_record_set_info(args)
    if response['message']['recordSets'] != []:
        global record_set_name, ip_address, record_set_id, zone_id
        record_set_name = response['message']['recordSets'][0]['name']
        ip_address = response['message']['recordSets'][0]['records'][0]['address']
        record_set_id = response['message']['recordSets'][0]['id']
        
    response = get_zone_info(args)
    if response['message']['zones'] != []:
        for i, zone in enumerate([d['name'] for d in response['message']['zones']]):
            if args.domain in zone:
                global zone_id
                zone_id = response['message']['zones'][i]['id']
        if zone_id is None:
            print (f"Zone with name {args.domain} doesn't exists")
            sys.exit()

def cli():
    try:
        parser = argparse.ArgumentParser(description='vinyldns - CLI to the VinylDNS DNS-as-a-service')
        
        subparsers = parser.add_subparsers(dest='option')

        get_zone_parser = subparsers.add_parser('get-zone-info', help='Get Zone Information')
        get_zone_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        get_zone_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')

        # get_record_parser = subparsers.add_parser('get-record-set-info', help='Get Record Set Information')
        # get_record_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        # get_record_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        # get_record_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        # get_record_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Record Set Name')

        search_record_parser = subparsers.add_parser('search-record-set-info', help='Search Record Set Information')
        search_record_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        search_record_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        search_record_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        search_record_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Domain name')

        create_record_parser = subparsers.add_parser('create-record-set', help='Create new Record Set')
        create_record_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        create_record_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        create_record_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        create_record_parser.add_argument('--record-set-ip', type=str, required=True, help = 'Vinyl Record Set IP Address')
        create_record_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Domain name')
        create_record_parser.add_argument('--ipcontrol-username', type=str, required=True, help = 'IP control username')
        create_record_parser.add_argument('--ipcontrol-password', type=str, required=True, help = 'IP control password')

        update_record_parser = subparsers.add_parser('update-record-set', help='Update the Record Set')
        update_record_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        update_record_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        update_record_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        update_record_parser.add_argument('--record-set-ip', type=str, required=True, help = 'Vinyl Record Set IP Address')
        update_record_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Domain name')
        update_record_parser.add_argument('--ipcontrol-username', type=str, required=True, help = 'IP control username')
        update_record_parser.add_argument('--ipcontrol-password', type=str, required=True, help = 'IP control password')

        delete_record_parser = subparsers.add_parser('delete-record-set', help='Delete the Record Set')
        delete_record_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        delete_record_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        delete_record_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        delete_record_parser.add_argument('--record-set-ip', type=str, required=True, help = 'Vinyl Record Set IP Address')
        delete_record_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Domain name')
        delete_record_parser.add_argument('--ipcontrol-username', type=str, required=True, help = 'IP control username')
        delete_record_parser.add_argument('--ipcontrol-password', type=str, required=True, help = 'IP control password')

        create_alias_parser = subparsers.add_parser('create-alias', help='Create the alias name for Record Set')
        create_alias_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        create_alias_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        create_alias_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        create_alias_parser.add_argument('--alias', type=str, required=True, help = 'Alias name for record set')
        create_alias_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Domain name')

        delete_alias_parser = subparsers.add_parser('delete-alias', help='Delete the alias name of Record Set')
        delete_alias_parser.add_argument('--access-key', type=str, required=True, help = 'Vinyl Access Key')
        delete_alias_parser.add_argument('--secret-key', type=str, required=True, help = 'Vinyl Secret Key')
        delete_alias_parser.add_argument('--record-set-name', type=str, required=True, help = 'Vinyl Record Set Name')
        delete_alias_parser.add_argument('--alias', type=str, required=True, help = 'Alias name for record set')
        delete_alias_parser.add_argument('--domain', type=str, required=True, help = 'Vinyl Domain name')
        
        args = parser.parse_args()

        if args.option == 'get-zone-info':
            print(get_zone_info(args))
        # if args.option == 'get-record-set-info':
        #     search_record(args)
        #     print(get_record_set_info(args, zone_id))
        if args.option == 'search-record-set-info':
            print(search_record_set_info(args))

        if args.option == 'create-record-set':
            search_record(args)
            if (record_set_name != args.record_set_name and ip_address != args.record_set_ip) or (record_set_name != args.record_set_name and ip_address == args.record_set_ip):
                create_response = create_record_set(args, zone_id)
                if create_response['statusCode'] == 202:
                    ip_login_response = login(args)
                    if ip_login_response['statusCode'] == 200:                                                        
                        access_token = ip_login_response['message']['access_token']
                        get_device_response = get_device(args.record_set_ip, access_token)
                        if get_device_response['statusCode'] == 200:
                            update_device_response = update_device(args, access_token, get_device_response['message']['id'], get_device_response['message']['interfaces'][0]['id'])
                            if update_device_response['statusCode'] == 200:
                                print(format_response(create_response['statusCode'], update_device_response['statusCode'], 'update', args))    
                            else:
                                print(format_response(create_response['statusCode'], update_device_response['statusCode'], 'update', args,  update_device_response['message']['faultString']))
                        elif get_device_response['statusCode'] == 400:
                            create_device_response = create_device(args, access_token)
                            print(format_response(create_response['statusCode'], create_device_response['statusCode'], 'create', args))
                        else:
                            print(format_response(create_response['statusCode'], get_device_response['statusCode'], 'create', args))
                else:
                    print(format_response(create_response['statusCode'], create_response['statusCode'], 'create', args))
            elif record_set_name == args.record_set_name and ip_address != args.record_set_ip:
                update_response = update_record_set(args, zone_id, record_set_id)
                if update_response['statusCode'] == 202:
                    ip_login_response = login(args)
                    if ip_login_response['statusCode'] == 200:
                        access_token = ip_login_response['message']['access_token']
                        get_device_response = get_device(ip_address, access_token)
                        if get_device_response['statusCode'] == 200:
                            update_device_response = update_device(args, access_token, get_device_response['message']['id'], get_device_response['message']['interfaces'][0]['id'])
                            if update_device_response['statusCode'] == 200:
                                print(format_response(update_response['statusCode'], update_device_response['statusCode'], 'update', args))    
                            else:
                                print(format_response(update_response['statusCode'], update_device_response['statusCode'], 'update', args,  update_device_response['message']['faultString']))
                        elif get_device_response['statusCode'] == 400:
                            create_device_response = create_device(args, access_token)
                            print(format_response(update_response['statusCode'], create_device_response['statusCode'], 'create', args))
                        else:
                            print(format_response(update_response['statusCode'], 404, 'update', args))
                else:
                    print(format_response(update_response['statusCode'], update_response['statusCode'], 'update', args))
            elif record_set_name == args.record_set_name and ip_address == args.record_set_ip:
                ip_login_response = login(args)
                if ip_login_response['statusCode'] == 200:                                                        
                    access_token = ip_login_response['message']['access_token']
                    get_device_response = get_device(args.record_set_ip, access_token)
                    create_device_response = create_device(args, access_token)
                    print(format_response(409, create_device_response['statusCode'], 'create', args, create_device_response['message']['faultString']))

        if args.option == 'delete-record-set':
            search_record(args)
            if record_set_name == args.record_set_name and ip_address == args.record_set_ip:
                delete_response = delete_record_set(args, zone_id, record_set_id)
                if delete_response['statusCode'] == 202:
                    ip_login_response = login(args)
                    if ip_login_response['statusCode'] == 200:
                        access_token = ip_login_response['message']['access_token']
                        delete_device_response = (delete_device(args, access_token))
                        print(format_response(delete_response['statusCode'], delete_device_response['statusCode'], 'delete', args))
            else:
                ip_login_response = login(args)
                if ip_login_response['statusCode'] == 200:                                                        
                    access_token = ip_login_response['message']['access_token']
                    delete_device_response = delete_device(args, access_token)
                    print(format_response(404, delete_device_response['statusCode'], 'delete', args, delete_device_response['message']['faultString']))

        if args.option == 'update-record-set':
            search_record(args)
            if record_set_name == args.record_set_name and ip_address != args.record_set_ip:
                update_response = update_record_set(args, zone_id, record_set_id)
                if update_response['statusCode'] == 202:
                    ip_login_response = login(args)
                    if ip_login_response['statusCode'] == 200:
                        access_token = ip_login_response['message']['access_token']
                        get_device_response = get_device(ip_address, access_token)
                        if get_device_response['statusCode'] == 200:
                            update_device_response = update_device(args, access_token, get_device_response['message']['id'], get_device_response['message']['interfaces'][0]['id'])
                            if update_device_response['statusCode'] == 200:
                                print(format_response(update_response['statusCode'], update_device_response['statusCode'], 'update', args))    
                            else:
                                print(format_response(update_response['statusCode'], update_device_response['statusCode'], 'update', args,  update_device_response['message']['faultString']))
                        else:
                            create_device_response = create_device(args, access_token)
                            print(format_response(update_response['statusCode'], create_device_response['statusCode'], 'update', args))
            elif record_set_name == args.record_set_name and ip_address == args.record_set_ip:
                ip_login_response = login(args)
                if ip_login_response['statusCode'] == 200:
                    access_token = ip_login_response['message']['access_token']
                    get_device_response = get_device(ip_address, access_token)
                    if get_device_response['statusCode'] == 200:
                        update_device_response = update_device(args, access_token, get_device_response['message']['id'], get_device_response['message']['interfaces'][0]['id'])
                        if update_device_response['statusCode'] == 200:
                            print(format_response(409, update_device_response['statusCode'], 'update', args))    
                        else:
                            print(format_response(409, update_device_response['statusCode'], 'update', args,  update_device_response['message']['faultString']))
                        
                    elif get_device_response['statusCode'] == 400:
                        create_device_response = create_device(args, access_token)
                        print(format_response(update_response['statusCode'], create_device_response['statusCode'], 'create', args))
            else:
                print(format_response(404, 404, 'update', args))
        
        if args.option == 'create-alias':
            search_record(args)
            if record_set_id is None:
                print(json.loads(json.dumps(
                                {
                                    "statusCode": 404,
                                    "message": f"Not Found - RecordSet with name {args.record_set_name} doesn't exists in zone {args.domain}",
                                    "name": args.record_set_name,
                                    "alias": args.alias,
                                    "domain": args.domain
                                }
                            )
                    ))
            else:
                search_alias_response = search_alias(args)
                if search_alias_response['message']['recordSets'] == []:
                    create_alias_response = create_alias(args, zone_id)
                    print(alias_response(create_alias_response['statusCode'], args, 'create'))
                else:
                    cname = search_alias_response['message']['recordSets'][0]['records'][0]['cname']   
                    if ''.join([args.record_set_name, '.', args.domain]) in cname:
                        print(''.join([args.record_set_name, '.', args.domain]))
                        print(cname)
                        print(alias_response(409, args, 'create'))
                    else:
                        delete_alias_response = (delete_record_set(args, search_alias_response['message']['recordSets'][0]['zoneId'], search_alias_response['message']['recordSets'][0]['id']))
                        if delete_alias_response['statusCode'] == 202:
                            create_alias_response = create_alias(args, zone_id)
                            print(alias_response(create_alias_response['statusCode'], args, 'create'))
                        else:
                            print(alias_response(404, args, 'create'))

        if args.option == 'delete-alias':
            search_alias_response = search_alias(args)
            if search_alias_response['message']['recordSets'] != []:
                fqdn = search_alias_response['message']['recordSets'][0]['fqdn']
                if ''.join([args.alias, '.', args.domain]) in fqdn:
                    delete_alias_response = delete_record_set(args, search_alias_response['message']['recordSets'][0]['zoneId'], search_alias_response['message']['recordSets'][0]['id'])
                    print(alias_response(delete_alias_response['statusCode'], args, 'delete'))
            else:
                print(alias_response(404, args, 'delete'))
                
    except Exception as e:
        return json.loads(json.dumps(
                                    {
                                        "statusCode": 500,
                                        "message": f"Exception has occurred with {e}",
                                    }
                                ))
            
if __name__ == "__main__":
    cli()
