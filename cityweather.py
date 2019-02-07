#!/usr/bin/python

# Copyright (C) 2011 Ian Gable
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

# Auth.: Ian Gable

import requests
import sys
from xml.etree.ElementTree import ElementTree, Element
from xml.etree import ElementTree as ETree


class CityIndex:
    def __init__(self):
        # this class could be changed to pass these two
        # hardcoded paths in
        self.city_list_url = "http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/siteList.xml"
        self.base_url = "http://dd.weatheroffice.ec.gc.ca/citypage_weather/xml/"
        self.cities = {}

        try:
            resp = requests.get(self.city_list_url)
        except requests.exceptions.RequestException:
            raise IOError("Unable to open the data url: " + self.city_list_url)

        # This passes the hole XML as a string, in production we should use a stream and ETree.parse() <-Nico
        city_list_tree = ETree.fromstring(resp.content)
        site_list = city_list_tree.findall("site")

        for site in site_list:
            city_name_english = site.findtext("nameEn")

            self.cities[city_name_english] = {
                'sitecode':     site.attrib['code'],
                'provincecode': site.findtext("provinceCode"),
                'nameFr':       site.findtext("nameFr")
            }

    def is_city(self, name):
        """
        Returns True if name is a valid city
        """
        return name in self.cities

    def data_url(self, name):
        """
        Returns resource URL for the city denoted by name
        """
        if self.is_city(name):
            return self.base_url + self.province(name) + "/" + self.site_code(name) + "_e.xml"
        return None

    def province(self, name):
        """
        Returns Province code (e.g. 'ON', 'BC', etc) of the city denoted by name
        """
        if self.is_city(name):
            return self.cities[name]['provincecode']
        return None

    def site_code(self, name):
        """
        Returns the environment canada site for a city. For example Athabasca, AB
        has the site code s0000001
        """
        if self.is_city(name):
            return self.cities[name]['sitecode']
        return None

    def french_name(self, name):
        if self.is_city(name):
            return self.cities[name]['nameFr']
        return None

    def english_city_list(self):
        return self.cities.keys()

    def french_city_list(self):
        return [v['nameFr'] for k, v in self.cities.items()]


class City:
    tree: Element

    # note that we are are grabbing a different
    # data URL then in city list

    def __init__(self, dataurl):
        try:
            resp = requests.get(dataurl)
        except requests.exceptions.RequestException:
            raise IOError("Unable to open the data url: " + dataurl)

        # This passes the hole XML as a string, in production we should use a stream and ETree.parse() <-Nico
        self.tree = ETree.fromstring(resp.content)

    def get_quantity(self, path):
        """Get the quatity contained at the XML XPath"""
        return self.tree.findtext(path)

    def get_attribute(self, path, attribute):
        """Get the attribute of the element at XPath path"""
        element = self.tree.find(path)
        if element is not None and attribute in element.attrib:
            return element.attrib[attribute]
        return None

    def get_available_quantities(self):
        """Get a list of all the available quatities in the form of their
        XML XPaths
        """

        pathlist = []
        # we are getting the full XPath with the attribute strings
        # this output is pretty long so maybe it would be wise
        # to also have an option to get the XPath without the attributes
        # self._get_all_xpaths(pathlist,"",self.tree.getroot())

        self._get_all_xpaths_with_attributes(pathlist, "", self.tree)
        return pathlist

    # This nasty little function recursively traverses
    # an element tree to get all the available XPaths
    # you have to pass in the pathlist you want to contain
    # the list
    def _get_all_xpaths(self, pathlist, path, element):
        children = element.getchildren()
        if not children:
            pathlist.append(path + "/" + element.tag)
        else:
            for child in children:
                self._get_all_xpaths(pathlist, path + "/" + element.tag, child)

    def _make_attribute_list(self, attrib):
        xpathattrib = ""
        for attribute, value in attrib.items():
            xpathattrib = xpathattrib + "[@" + attribute + "='" + value + "']"
        return xpathattrib

    # This nasty little function recursively traverses
    # an element tree to get all the available XPaths
    # you have to pass in the pathlist you want to contain
    # the list
    def _get_all_xpaths_with_attributes(self, pathlist, path, element):
        children = element.getchildren()
        if not children:
            xpathattrib = self._make_attribute_list(element.attrib)

            if path == "":
                pathlist.append(element.tag + xpathattrib)
            else:
                pathlist.append(path + "/" + element.tag + xpathattrib)

        else:
            xpathattrib = self._make_attribute_list(element.attrib)

            for child in children:
                # skip the root tag
                if element.tag == "siteData":
                    self._get_all_xpaths_with_attributes(pathlist, path, child)
                else:
                    # we avoid the opening / since we start below the root
                    if path == "":
                        self._get_all_xpaths_with_attributes(pathlist, element.tag + xpathattrib, child)
                    else:
                        self._get_all_xpaths_with_attributes(pathlist, path + "/" + element.tag + xpathattrib, child)

    # This function will break is thre is any change in the city weather
    # XML format
    def get_available_forecast_names(self):
        forecasts = self.tree.findall('forecastGroup/forecast/period')
        forecastnames = []
        for forecast in forecasts:
            forecastnames.append(forecast.get("textForecastName"))
        return forecastnames

    # This function will break is thre is any change in the city weather
    # XML format
    def get_available_forecast_periods(self):
        forecasts = self.tree.findall('forecastGroup/forecast/period')
        forecastnames = []
        for forecast in forecasts:
            forecastnames.append(forecast.text)
        return forecastnames

