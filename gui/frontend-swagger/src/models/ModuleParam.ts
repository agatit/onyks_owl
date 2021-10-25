// tslint:disable
/**
 * Onyks Wagon Location API
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import {
    Module,
    ModuleFromJSON,
    ModuleToJSON,
    ModuleParamDef,
    ModuleParamDefFromJSON,
    ModuleParamDefToJSON,
} from './';

/**
 * List of all parameters availaible for module filled with values from specified config.json or default values
 * @export
 * @interface ModuleParam
 */
export interface ModuleParam  {
    /**
     * 
     * @type {string}
     * @memberof ModuleParam
     */
    paramDefId: string;
    /**
     * 
     * @type {string}
     * @memberof ModuleParam
     */
    value?: string;
    /**
     * 
     * @type {Module}
     * @memberof ModuleParam
     */
    module?: Module;
    /**
     * 
     * @type {ModuleParamDef}
     * @memberof ModuleParam
     */
    paramDef?: ModuleParamDef;
}

export function ModuleParamFromJSON(json: any): ModuleParam {
    return {
        'paramDefId': json['param_def_id'],
        'value': !exists(json, 'value') ? undefined : json['value'],
        'module': !exists(json, 'module') ? undefined : ModuleFromJSON(json['module']),
        'paramDef': !exists(json, 'param_def') ? undefined : ModuleParamDefFromJSON(json['param_def']),
    };
}

export function ModuleParamToJSON(value?: ModuleParam): any {
    if (value === undefined) {
        return undefined;
    }
    return {
        'param_def_id': value.paramDefId,
        'value': value.value,
        'module': ModuleToJSON(value.module),
        'param_def': ModuleParamDefToJSON(value.paramDef),
    };
}


